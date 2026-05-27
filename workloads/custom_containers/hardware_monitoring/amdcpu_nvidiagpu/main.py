#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# This is for Linux devices running on AMD CPUs
# CLI instructions file_name + <MQTT topic name as a string>
# + <Integer for sleep interval>
# e.g., python3 monitor_amd_linux.py '/home/amd' 5
import gc
import json
import logging
import os
import sys
from time import sleep

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.amd_apu import AMDCPUData  # noqa: E402
from hw_monitoring_libraries.nvidia_gpu import NvidiaSensors  # noqa: E402
from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.hw_monitoring\
    import MonitoringUtilities  # noqa: E402


def monitor(client: object, get_data: object,
            gpu_data: object,
            TOPIC: str,
            INTERVAL: int):

    while True:

        # get CPU utilization
        cpu_util = get_data.get_cpu_data()

        # get current RAM use
        ram_util = get_data.get_ram_data()

        # get current freq and core count
        cpu_freq, core_count = get_data.get_freq()

        # get CPU, iGPU and NVME temperatures
        nvme_temp, cpu_temp, amdgpu_temp = get_data.amd_linux_temp_data()

        # get NVIDIA data
        # get GPU data
        gpu_temp, gpu_load, gpu_vram, gpu_power, gpu_clock = gpu_data.\
            gpu_query()

        payload = {
            "cpu_temp": cpu_temp,
            "amdgpu_temp": amdgpu_temp,
            "nvme_temp": nvme_temp,
            "cpu_freq": cpu_freq,
            "cpu_use": cpu_util,
            "ram_use": ram_util,
            "gpu_temp": gpu_temp,
            "gpu_load": gpu_load,
            "gpu_vram": gpu_vram,
            "gpu_power": gpu_power,
            "gpu_clock": gpu_clock
        }

        payload = json.dumps(payload)
        # logger.info(payload)

        result = client.publish(TOPIC, payload)
        status = result[0]

        if status != 0:
            print(f'Failed to send {payload} to: {TOPIC}')
            logging.debug(f'MQTT publishing failure, return code: {status}')

        del payload, cpu_temp, amdgpu_temp, nvme_temp, cpu_freq, \
            cpu_util, ram_util, status, result
        gc.collect()

        sleep(INTERVAL)


def main():

    # instantiate utilities class
    monitor_utilities = MonitoringUtilities()

    TOPIC = os.environ['TOPIC']
    INTERVAL = int(os.environ['INTERVAL'])

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    client_id = monitor_utilities.getClientID()

    # get mqtt client
    client, code = monitor_utilities.mqttClient(client_id,
                                                MQTT_USER,
                                                MQTT_SECRET,
                                                MQTT_BROKER,
                                                MQTT_PORT)

    # instantiate CPU & GPU data classes
    get_data = AMDCPUData()

    # gpu monitoring class
    gpu_data = NvidiaSensors()
    logger.info('CPU & GPU monitoring classes instantiated')

    # start data monitoring
    try:
        monitor(client, get_data, gpu_data, TOPIC, INTERVAL)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
