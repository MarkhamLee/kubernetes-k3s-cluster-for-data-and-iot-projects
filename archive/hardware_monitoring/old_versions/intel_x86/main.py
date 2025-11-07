#!/usr/bin/env python
# Markham Lee (C) 2023
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor CPU and NVME temp, plus RAM and CPU
# utilization on the x86 based nodes.
import gc
import os
import sys
from time import sleep
from intel_x86 import Intelx86

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.influx_client import InfluxClient  # noqa: E402

# instantiate InfluxDB class
influxdb_write = InfluxClient()


def get_base_payload(table):

    # base payload
    base_payload = {
        "measurement": table,
        "tags": {
                "k3s_prod": "hardware_telemetry",
        }
    }

    return base_payload


def monitor(client: object, BUCKET: str, INTERVAL: int, base_payload: dict):

    # instantiate utilities class
    device_data = Intelx86()

    DEVICE_ID = os.environ['DEVICE_ID']
    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        try:

            # get CPU utilization
            cpu_util = device_data.get_cpu_data()

            # get current RAM use
            ram_use = device_data.get_ram_data()

            # get avg clock speed for all cores
            cpu_freq, core = device_data.get_freq()

            # get CPU temperature
            cpu_temp, nvme_temp = device_data.get_temp()

            payload = {
                "cpu_utilization": cpu_util,
                "ram_utilization": ram_use,
                "cpu_freq": cpu_freq,
                "cpu_temp": cpu_temp,
                "nvme_temp": nvme_temp,
                "count_count": core
            }

            # write data to InfluxDB
            influxdb_write.write_influx_data(client, base_payload,
                                             payload, BUCKET)

            del cpu_util, ram_use, cpu_freq, core, cpu_temp, nvme_temp, payload
            gc.collect()

        except Exception as e:

            logger.debug(f'failed to read data from device with error: {e}')
            # we'll just log the errors for now, if the device is truly
            # malfunctioning alert manager will pick it up as a
            # node error/problem.

        sleep(INTERVAL)


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']
    INTERVAL = os.environ['INTERVAL']

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    # get base payload
    base_payload = get_base_payload(TABLE)

    monitor(client, BUCKET, INTERVAL, base_payload)


if __name__ == '__main__':
    main()
