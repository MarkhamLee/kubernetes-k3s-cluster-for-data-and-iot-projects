# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Script for monitoring a Raspberry Pi 4B, pulling CPU utilization,
# temps and clock speed and RAM utilization data. The Data is transmitted
# via MQTT because it a) uses less power than API requests b) the
# communication is two way, which will be used to light up future device
# mgt capabilities in the future.
import gc
import json
import os
import sys
import time
from rpi4b_data import Rpi4bData

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.hw_monitoring\
    import MonitoringUtilities  # noqa: E402


# method that runs monitoring loop
def monitor(client: object, getData: object, topic: str):

    DEVICE_ID = os.environ['DEVICE_ID']
    INTERVAL = int(os.environ['INTERVAL'])

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        # get CPU utilization
        cpuUtil = getData.getCPUData()

        # get current RAM use
        ramUse = getData.getRamData()

        # get current freq and core count
        cpuFreq, coreCount = getData.getFreq()

        # get CPU temperature
        cpuTemp = getData.get_rpi4b_temps()

        payload = {
            "cpuTemp": cpuTemp,
            "cpuFreq": cpuFreq,
            "cpuUse": cpuUtil,
            "ramUse": ramUse
        }

        payload = json.dumps(payload)
        result = client.publish(topic, payload)
        status = result[0]

        if status != 0:

            logger.debug(f'MQTT publishing failure for hardware monitoring on: {DEVICE_ID}, return code: {status}')  # noqa: E501

        del payload, cpuUtil, ramUse, cpuFreq, cpuTemp, status, result
        gc.collect()
        time.sleep(INTERVAL)


def main():

    # instantiate RPI4B data retrieval class
    get_data = Rpi4bData()
    logger.info('Data class instantiated')

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
        monitor(client, get_data, TOPIC)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
