# Markham Lee (C) 2023 - 2025
# Homelab & Selfhosting Toolkit
# https://github.com/MarkhamLee/homelab-and-self-hosting-toolkit
# HW monitoring Script for an Orange Pi 5+, customized for the chipset
# vs the more generic and often "somewhat off" data you'd get from
# something like Prometheus. However, there is also an option to
# to create a Proemetheus scrape target to collect "heartbeat" data
# This script "should work" on any device running a Rockchip 3588
# System on Chip (SOC). But it was specifically built and tested \
# on an Orange Pi 5+.
import os
import sys
from prometheus_client import Gauge, start_http_server
from time import sleep
from rockchip_3588 import RockChipData

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402
from hw_monitoring_libraries.influx_client import InfluxClient  # noqa: E402
from hw_monitoring_libraries.\
    hw_monitoring import MonitoringUtilities  # noqa: E402

hw_utilities = MonitoringUtilities()

# instantiate InfluxDB class
influxdb_write = InfluxClient()


# instantiate hardware data class
rockchip_data = RockChipData()

# load environmental variables
BUCKET = os.environ['INFLUX_BUCKET']
DEVICE_ID = os.environ['DEVICE_ID']
HEARTBEAT_FLAG = int(os.environ['HEARTBEAT_FLAG'])
INTERFACE_NAME = os.environ['INTERFACE_NAME']
INTERVAL = int(os.environ['INTERVAL'])
METRIC_IP = os.environ['METRIC_IP']
METRIC_PORT = int(os.environ['METRIC_PORT'])
ORG = os.environ['INFLUX_ORG']
TABLE = os.environ['INFLUX_MEASUREMENT']
TOKEN = os.environ['INFLUX_TOKEN']
URL = os.environ['INFLUX_URL']
TAG_KEY = os.environ['TAG_KEY']
TAG_VALUE = os.environ['TAG_VALUE']
UPTIME_KUMA_FLAG = int(os.environ['UPTIME_KUMA_FLAG'])
UPTIME_KUMA_WEBHOOK = os.environ['UPTIME_KUMA_WEBHOOK']

logger.info('Creating base payload for writing to InfluxDB')
base_payload = {
    "measurement": TABLE,
    "tags": {
            TAG_KEY: TAG_VALUE,
    }
}

# if Prometheus flag is setup, turn on web server for exporting
# hearbeat data

if HEARTBEAT_FLAG == 1:
    logger.info('Settiing up Prometheus heartbeat metric export')
    METRIC_NAME = (f'{DEVICE_ID}_HEARTBEAT')
    heartbeat = Gauge(METRIC_NAME, DEVICE_ID)

    logger.info('Starting metric server')
    start_http_server(METRIC_PORT, addr=METRIC_IP)


def monitor(client: object):

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        try:
            # get CPU utilization
            cpu_util = rockchip_data.get_cpu_data()

            # get current RAM use
            ram_use = rockchip_data.get_ram_data()

            # get per CPU frequencies (bigCore0, bigCore1, littleCore)
            little_core_freq, big_core0_freq, big_core1_freq = rockchip_data.\
                get_rockchip_3588_freqs()

            # get system temperatures
            soc_temp, big_core0_temp, big_core1_temp, little_core_temp, \
                center_temp, gpu_temp, npu_temp, \
                nvme_temp = rockchip_data.sys_temps()

            # get CPU load average
            five_min_avg, fifteen_min_avg = rockchip_data.get_load_average()

            # get ethernet connection speed
            ethernet_speed = rockchip_data.ethernet_data(INTERFACE_NAME)

            payload = {
                "SOC": soc_temp,
                "bigCore0": big_core0_temp,
                "bigCore1": big_core1_temp,
                "littleCore": little_core_temp,
                "Center": center_temp,
                "GPU": gpu_temp,
                "NPU": npu_temp,
                "NVME": nvme_temp,
                "littleCoreFreq": little_core_freq,
                "bigCore0Freq": big_core0_freq,
                "bigCore1Freq": big_core1_freq,
                "cpuUse": cpu_util,
                "ramUse": ram_use,
                "five_min_avg": five_min_avg,
                "fifteen_min_avg": fifteen_min_avg,
                "ethernet_speed": ethernet_speed
            }

            if UPTIME_KUMA_FLAG == 1:
                hw_utilities.send_uptime_kuma_heartbeat(UPTIME_KUMA_WEBHOOK,
                                                        DEVICE_ID)

            if HEARTBEAT_FLAG == 1:
                heartbeat.set(1)

            # write data to InfluxDB
            influxdb_write.write_influx_data(client,
                                             base_payload,
                                             payload,
                                             BUCKET)

        except Exception as e:
            logger.debug(f'Data read loop failed with error: {e}')
            # we'll just log the errors for now, if the device is truly
            # malfunctioning alert manager will pick it up as a
            # target down error/problem.

        sleep(INTERVAL)


def main():

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client)


if __name__ == '__main__':
    main()
