# Markham Lee (C) 2023 - 2026
# Private Cloud & Self Hosting with K3s
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor AMD hardware, and also provide
# (if needed) a Prometheus endpoint for collecting
import os
import sys
from prometheus_client import Gauge, start_http_server
from time import sleep
from amd64_apu import AMD64Data  # TODO: move this joint library folder

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.influx_client import InfluxClient  # noqa: E402


# load environmental variables
BUCKET = os.environ['INFLUX_BUCKET']
DEVICE_ID = os.environ['DEVICE_ID']
HEARTBEAT_FLAG = int(os.environ['HEARTBEAT_FLAG'])
INTERVAL = int(os.environ['INTERVAL'])
METRIC_IP = os.environ['METRIC_IP']
METRIC_PORT = int(os.environ['METRIC_PORT'])
ORG = os.environ['INFLUX_ORG']
TABLE = os.environ['INFLUX_MEASUREMENT']
TOKEN = os.environ['INFLUX_TOKEN']
URL = os.environ['INFLUX_URL']
TAG_KEY = os.environ['TAG_KEY']
TAG_VALUE = os.environ['TAG_VALUE']

logger.info('Creating base payload for writing to InfluxDB')
base_payload = {
    "measurement": TABLE,
    "tags": {
            TAG_KEY: TAG_VALUE,
    }
}

# instantiate InfluxDB class
influxdb_write = InfluxClient()

# instantiate device data class
device_data = AMD64Data()
logger.info("Hardware monitoring class instantiated")


# if Prometheus flag is setup, turn on web server for exporting
# hearbeat data
if HEARTBEAT_FLAG == 1:
    logger.info('Setting up Prometheus heartbeat metric export')
    METRIC_NAME = (f'{DEVICE_ID}_HEARTBEAT')
    heartbeat = Gauge(METRIC_NAME, DEVICE_ID)

    logger.info('Starting metric server')
    start_http_server(METRIC_PORT, addr=METRIC_IP)


def monitor(client: object):

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        try:

            # get CPU, GPU and NVME temperatures
            nvme_temp, cpu_temp, amd_gpu_temp = device_data.\
                amd_linux_temp_data()

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

            # write data to InfluxDB
            influxdb_write.write_influx_data(client,
                                             base_payload,
                                             payload,
                                             BUCKET)
            if HEARTBEAT_FLAG == 1:
                heartbeat.set(1)

        except Exception as e:
            logger.info(f'Data read loop failed with error: {e}')

        sleep(INTERVAL)


def main():

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client)


if __name__ == '__main__':
    main()
