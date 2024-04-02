# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-platform
# HW monitoring Script for an Orange Pi 5+, meant to extend the
# monitoring capabilities in K8s, namely: tracking CPU, NVME and GPU temps
#  & utilization data. This script "should work" on any device running
# a Rockchip 3588 System on Chip (SOC). But it was specifically built and
# tested on an Orange Pi 5 Plus Running Joshua Riek's Ubuntu Distro for
# RockChip 3588 Devices: https://github.com/Joshua-Riek/ubuntu-rockchip
import gc
import os
import sys
import time
from rockchip_3588 import RockChipData

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


def monitor(client: object, bucket: str, interval: int, base_payload: dict):

    # instantiate hardware data class
    rockchip_data = RockChipData()

    while True:

        logger.info("Starting HW data logging...")

        try:
            # get CPU utilization
            cpuUtil = rockchip_data.getCPUData()

            # get current RAM use
            ramUse = rockchip_data.getRamData()

            # get per CPU frequencies (bigCore0, bigCore1, littleCore)
            littleCoreFreq, bigCore0Freq, bigCore1Freq = rockchip_data.\
                getRockChip3588Freqs()

            # get system temperatures
            socTemp, bigCore0Temp, bigCore1Temp, littleCoreTemp, centerTemp, \
                gpuTemp, npuTemp, nvmeTemp = rockchip_data.sysTemps()

            payload = {
                "SOC": socTemp,
                "bigCore0": bigCore0Temp,
                "bigCore1": bigCore1Temp,
                "littleCore": littleCoreTemp,
                "Center": centerTemp,
                "GPU": gpuTemp,
                "NPU": npuTemp,
                "NVME": nvmeTemp,
                "littleCoreFreq": littleCoreFreq,
                "bigCore0Freq": bigCore0Freq,
                "bigCore1Freq": bigCore1Freq,
                "cpuUse": cpuUtil,
                "ramUse": ramUse
            }

            # write data to InfluxDB
            influxdb_write.write_influx_data(client, base_payload,
                                             payload, bucket)

            del payload, socTemp, bigCore0Temp, bigCore1Temp, \
                littleCoreTemp, centerTemp, gpuTemp, npuTemp, nvmeTemp,
            littleCoreFreq, bigCore0Freq, bigCore1Freq, cpuUtil, ramUse
            gc.collect()

        except Exception as e:
            logger.debug(f'failed to read data from device with error: {e}')
            # we'll just log the errors for now, if the device is truly
            # malfunctioning alert manager will pick it up as a
            # node error/problem.

        time.sleep(interval)


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']
    INTERVAL = int(os.environ['INTERVAL'])

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    # get base payload
    payload = get_base_payload(TABLE)

    monitor(client, BUCKET, INTERVAL, payload)


if __name__ == '__main__':
    main()
