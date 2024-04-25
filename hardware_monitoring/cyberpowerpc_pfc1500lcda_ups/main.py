# Markham Lee (C) 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Script for pulling leveraging the Network Ups Tools (NUT) application to
# to pull data from an UPS device connected to a small server running the
# NUT server. Running this requires the NUT client to installed on the
# machine running it
import gc
import json
import os
import sys
from time import sleep
import subprocess as sp


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.hw_monitoring\
    import MonitoringUtilities  # noqa: E402

UPS_ID = os.environ['UPS_ID']


# start monitoring loop
def ups_monitoring(CMD: str, TOPIC: str, client: object):

    INTERVAL = int(os.environ['UPS_INTERVAL'])

    logger.info(f'Starting monitoring for {UPS_ID}')

    while True:

        try:

            # query the UPS via bash to acquire data
            data = sp.check_output(CMD, shell=True)
            data = data.decode("utf-8").strip().split("\n")

            # parse data into a list of lists, each pair of values becomes
            # its own lists.
            initial_list = [i.split(':') for i in data]

            test_dict = dict(initial_list)

            # payload for MQTT message
            payload = {
                "battery_level": float(test_dict['battery.charge']),
                "battery_run_time":
                    (float(test_dict['battery.runtime']))/60,
                "battery_voltage": float(test_dict['battery.voltage']),
                "input_voltage": float(test_dict['input.voltage']),
                "load_percentage": float(test_dict['ups.load']),
                "max_power": float(test_dict['ups.realpower.nominal']),
                "ups_status": test_dict['ups.status'],
                "device_model": test_dict['device.model']
            }

            # build json payload
            payload = json.dumps(payload)

            result = client.publish(TOPIC, payload)
            status = result[0]

            if status != 0:
                logger.debug(f'MQTT publishing failure for monitoring UPS: {UPS_ID}, return code: {status}')  # noqa: E501

            del data, initial_list, test_dict, payload, result, status
            gc.collect()

        except Exception as e:
            logger.debug(f'Failed to read data from UPS: {UPS_ID} with error: {e}')  # noqa: E501
            # TODO: add Slack alert for when UPS goes down, low priority right
            # now as the Firewall will send an alert if the UPS goes down
            sleep(600)

        sleep(INTERVAL)


def build_query():

    UPS_IP = os.environ['UPS_IP']

    CMD = "upsc " + UPS_ID + "@" + UPS_IP

    return CMD


def main():

    # instantiate hardware monitoring class
    monitor_utilities = MonitoringUtilities()
    logger.info('Monitoring utilities class instantiated')

    # operating parameters
    TOPIC = os.environ['UPS_TOPIC']

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    CMD = build_query()

    # get unique client ID
    clientID = monitor_utilities.getClientID()

    # get mqtt client
    client, code = monitor_utilities.mqttClient(clientID,
                                                MQTT_USER, MQTT_SECRET,
                                                MQTT_BROKER, MQTT_PORT)

    # start monitoring
    try:
        ups_monitoring(CMD, TOPIC, client)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
