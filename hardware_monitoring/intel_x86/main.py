#!/usr/bin/env python
# Markham Lee (C) 2023
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor CPU and NVME temp, plus RAM and CPU
# utilization on the x86 based nodes.
import gc
import json
import os
import sys
from time import sleep
from intel_x86 import Intelx86

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.hw_monitoring\
    import MonitoringUtilities  # noqa: E402


# monitoring loop
def monitor(client: object, topic: str):

    # instantiate utilities class
    device_data = Intelx86()

    DEVICE_ID = os.environ['DEVICE_ID']
    INTERVAL = int(os.environ['INTERVAL'])

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        # get CPU utilization
        cpu_util = device_data.get_cpu_data()

        # get current RAM use
        ram_use = device_data.get_ram_data()

        # get avg clock speed for all cores
        cpu_freq, core = device_data.get_freq()

        # get CPU temperature
        cpu_temp, nvme_temp = device_data.get_temps()

        payload = {
            "cpu_utilization": cpu_util,
            "ram_utilization": ram_use,
            "cpu_freq": cpu_freq,
            "cpu_temp": cpu_temp,
            "nvme_temp": nvme_temp,
            "core_count": core
        }

        payload = json.dumps(payload)
        result = client.publish(topic, payload)
        status = result[0]

        if status != 0:

            logger.debug(f'MQTT publishing failure for hardware monitoring on: {DEVICE_ID}, return code: {status}')  # noqa: E501

        del payload, cpu_util, ram_use, cpu_freq, cpu_temp, status, result
        gc.collect()
        sleep(INTERVAL)


def main():

    # instantiate hardware monitoring class
    monitor_utilities = MonitoringUtilities()
    logger.info('Monitoring utilities class instantiated')

    # operating parameters
    TOPIC = os.environ['TOPIC']

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    clientID = monitor_utilities.getClientID()

    # get mqtt client
    client, code = monitor_utilities.mqttClient(clientID,
                                                MQTT_USER, MQTT_SECRET,
                                                MQTT_BROKER, MQTT_PORT)

    # start monitoring
    try:
        monitor(client, TOPIC)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
