#!/usr/bin/env python
# Markham Lee (C) 2023 - 2024
# K3s-Data-Platform-IoT
# https://github.com/MarkhamLee/kubernetes-k3s-data-platform-IoT
# This script "should work" on any device running a Rockchip 3588
# System on Chip (SOC). But it was specifically built and tested on
# an Orange Pi 5 Plus Running Joshua Riek's Ubuntu Distro for
# RockChip 3588 Devices:
# https://github.com/Joshua-Riek/ubuntu-rockchip


import time
import gc
import os
import logging
from sys import stdout
from rockchip_3588 import RockChipData
from influx_client import InfluxClient

# set up/configure logging with stdout so it can be picked up by K8s
logger = logging.getLogger('rockchip_telemetry_logger')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')  # noqa: E501
handler.setFormatter(formatter)
logger.addHandler(handler)

# instantiate InfluxDB class
influxdb_write = InfluxClient()


def monitor(client: object, bucket, table, interval):

    # base payload
    base_payload = {
        "measurement": table,
        "tags": {
                "k3s_prod": "hardware_telemetry",
        }
    }

    # instantiate hardware data class
    rockchip_data = RockChipData()

    while True:

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

    monitor(client, BUCKET, TABLE, INTERVAL)


if __name__ == '__main__':
    main()
