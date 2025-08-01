#!/usr/bin/env python
# Markham Lee (C) 2023 - 2025
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor CPU and NVME temp, plus RAM and CPU
# utilization on x86 hardware.
import os
import sys
from prometheus_client import Gauge, start_http_server
from time import sleep

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.intel_x86 import Intelx86  # noqa: E402
from hw_monitoring_libraries.influx_client import InfluxClient  # noqa: E402

# instantiate InfluxDB class
influxdb_write = InfluxClient()

# hardware monitoring class
device_data = Intelx86()
logger.info('Monitoring utilities class instantiated')

# load environmental variables
BUCKET = os.environ['INFLUX_BUCKET']
DEVICE_ID = os.environ['DEVICE_ID']
HEARTBEAT_FLAG = int(os.environ['HEARTBEAT_FLAG'])
INTERVAL = int(os.environ['INTERVAL'])
ORG = os.environ['INFLUX_ORG']
TABLE = os.environ['INFLUX_MEASUREMENT']
TOKEN = os.environ['INFLUX_TOKEN']
URL = os.environ['INFLUX_URL']

logger.info('Creating base payload for writing to InfluxDB')
base_payload = {
    "measurement": TABLE,
    "tags": {
            "k3s_prod": "hardware_telemetry",
    }
}

# if Prometheus flag is setup, turn on web server for exporting
# hearbeat data

if HEARTBEAT_FLAG == 1:
    logger.info('Settiing up Prometheus heartbeat metric export')
    METRIC_NAME = (f'{DEVICE_ID}_HEARTBEAT')
    heartbeat = Gauge(METRIC_NAME, DEVICE_ID)

    IP = os.environ['METRIC_IP']

    logger.info('Starting metric server')
    start_http_server(5011, addr=IP)


# monitoring loop
def monitor(client: str):

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

        # write data to InfluxDB
        influxdb_write.write_influx_data(client,
                                         base_payload,
                                         payload,
                                         BUCKET)
        heartbeat.set(1)
        sleep(INTERVAL)


def main():

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client)


if __name__ == '__main__':
    main()
