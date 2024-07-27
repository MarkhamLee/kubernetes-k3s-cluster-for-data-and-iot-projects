# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor temperatures of the AMD 5560u on the
# Beelink SER5s that are being used for the cluster nodes.
# Only monitoring the temps (for now), because I'm using the
# kube-prometheus stack to monitor CPU load, disk space, RAM, etc.
import gc
import json
import os
import sys
from time import sleep
from amd_5560u import AMD5560Data

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.hw_monitoring\
    import MonitoringUtilities  # noqa: E402


def monitor(client: object, topic: str):

    # instantiate utilities class
    device_data = AMD5560Data()

    logger.info("Hardware monitoring class instantiated")

    DEVICE_ID = os.environ['DEVICE_ID']
    INTERVAL = int(os.environ['INTERVAL'])

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        # get CPU, GPU and NVME temperatures
        nvme_temp, cpu_temp, amd_gpu_temp = device_data.amd_linux_temp_data()

        cpu_util = device_data.get_cpu_data()

        cpu_freq, core_count = device_data.get_freq()

        ram_util = device_data.get_ram_data()

        payload = {
            "nvme_temp": nvme_temp,
            "cpu_temp": cpu_temp,
            "amd_gpu_temp": amd_gpu_temp,
            "cpu_util": cpu_util,
            "cpu_freq": cpu_freq,
            "ram_util": ram_util,
            "core_count": core_count
        }

        print(payload)

        payload = json.dumps(payload)
        result = client.publish(topic, payload)
        status = result[0]

        if status != 0:

            logger.debug(f'MQTT publishing failure for hardware monitoring on: {DEVICE_ID}, return code: {status}')  # noqa: E501

        del payload, cpu_util, ram_use, cpu_freq, cpu_temp, status, result
        gc.collect()
        sleep(INTERVAL)


def main():

    # instantiate communication utilities class
    monitor_utilities = MonitoringUtilities()

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
