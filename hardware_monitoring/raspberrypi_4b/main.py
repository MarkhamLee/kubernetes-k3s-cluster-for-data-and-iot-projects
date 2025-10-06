# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Script for monitoring a Raspberry Pi 4B, pulling CPU utilization,
# temps and clock speed and RAM utilization data.
import os
import sys
import time
from prometheus_client import Gauge, start_http_server
from rpi4b_data import Rpi4bData

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.\
    logging_util import logger  # noqa: E402
from hw_monitoring_libraries.\
    influx_client import InfluxClient  # noqa: E402

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

# instantiate InfluxDB class
influxdb_write = InfluxClient()

# instantiate RPI4B data retrieval class
get_data = Rpi4bData()
logger.info('Data class instantiated')


logger.info('Creating base payload for writing to InfluxDB')
base_payload = {
    "measurement": TABLE,
    "tags": {
            TAG_KEY: TAG_VALUE,
    }
}


if HEARTBEAT_FLAG == 1:
    logger.info('Settiing up Prometheus heartbeat metric export')
    METRIC_NAME = (f'{DEVICE_ID}_HEARTBEAT')
    heartbeat = Gauge(METRIC_NAME, DEVICE_ID)

    logger.info('Starting metric server')
    start_http_server(METRIC_PORT, addr=METRIC_IP)


# method that runs monitoring loop
def monitor(client: object):

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        # get CPU utilization
        cpu_util = get_data.get_cpu_data()

        # get current RAM use
        ram_use = get_data.get_ram_data()

        # get current freq and core count
        cpu_freq, core_count = get_data.get_freq()

        # get CPU temperature
        cpu_temp = get_data.get_rpi4b_temps()

        payload = {
            "cpuTemp": cpu_temp,
            "cpuFreq": cpu_freq,
            "cpuUse": cpu_util,
            "ramUse": ram_use
        }

        # write data to InfluxDB
        influxdb_write.write_influx_data(client,
                                         base_payload,
                                         payload,
                                         BUCKET)

        if HEARTBEAT_FLAG == 1:
            heartbeat.set(1)

        time.sleep(INTERVAL)


def main():

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client)


if __name__ == '__main__':
    main()
