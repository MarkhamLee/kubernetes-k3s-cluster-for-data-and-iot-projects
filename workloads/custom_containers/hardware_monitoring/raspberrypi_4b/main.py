# Markham Lee (C) 2023 - 2026
# K3s Powered Private Cloud
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script for monitoring a Raspberry Pi 4B, pulling CPU utilization,
# temps, clock speed and RAM utilization data. There is also an
# option to surface a Prometheus scrape point and push "heartbeats"
# to Uptime Kuma, for the purposes of receiving near real time alerts
# if the device goes down.
import os
import sys
import time
from prometheus_client import Gauge, start_http_server

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.\
    logging_util import logger  # noqa: E402
from hw_monitoring_libraries.\
    influx_client import InfluxClient  # noqa: E402
from hw_monitoring_libraries.rpi_data import RpiData  # noqa: E402
from hw_monitoring_libraries.\
    hw_monitoring import MonitoringUtilities  # noqa: E402

hw_utilities = MonitoringUtilities()

# load environmental variables
BUCKET = os.environ['INFLUX_BUCKET']
DEVICE_ID = os.environ['DEVICE_ID']
INTERFACE_NAME = os.environ['INTERFACE_NAME']
INTERVAL = int(os.environ['INTERVAL'])
METRIC_IP = os.environ['METRIC_IP']
METRIC_PORT = int(os.environ['METRIC_PORT'])
ORG = os.environ['INFLUX_ORG']
PROMETHEUS_HEARTBEAT_FLAG = os.environ['PROMETHEUS_HEARTBEAT_FLAG']
TABLE = os.environ['INFLUX_MEASUREMENT']
TOKEN = os.environ['INFLUX_TOKEN']
URL = os.environ['INFLUX_URL']
TAG_KEY = os.environ['TAG_KEY']
TAG_VALUE = os.environ['TAG_VALUE']
UPTIME_KUMA_FLAG = int(os.environ['UPTIME_KUMA_FLAG'])
UPTIME_KUMA_WEBHOOK = os.environ['UPTIME_KUMA_WEBHOOK']

# instantiate InfluxDB class
influxdb_write = InfluxClient()

# instantiate RPI data retrieval class
get_data = RpiData()
logger.info('Data class instantiated')


logger.info('Creating base payload for writing to InfluxDB')
base_payload = {
    "measurement": TABLE,
    "tags": {
            TAG_KEY: TAG_VALUE,
    }
}


if PROMETHEUS_HEARTBEAT_FLAG == 1:
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
        cpu_temp = get_data.get_cpu_temps()

        # get CPU load average
        five_min_avg, fifteen_min_avg = get_data.get_load_average()

        # get ethernet connection speed
        ethernet_speed = get_data.ethernet_data(INTERFACE_NAME)

        payload = {
            "cpu_temp": cpu_temp,
            "cpu_freq": cpu_freq,
            "cpu_use": cpu_util,
            "ram_use": ram_use,
            "five_min_avg": five_min_avg,
            "fifteen_min_avg": fifteen_min_avg,
            "connection_speed": ethernet_speed
        }

        if PROMETHEUS_HEARTBEAT_FLAG == 1:
            heartbeat.set(1)

        if UPTIME_KUMA_FLAG == 1:
            hw_utilities.send_uptime_kuma_heartbeat(UPTIME_KUMA_WEBHOOK,
                                                    DEVICE_ID)

        # write data to InfluxDB
        influxdb_write.write_influx_data(client,
                                         base_payload,
                                         payload,
                                         BUCKET)

        time.sleep(INTERVAL)


def main():

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client)


if __name__ == '__main__':
    main()
