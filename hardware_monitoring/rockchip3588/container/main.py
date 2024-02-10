#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# This script is specific to the Orange Pi 5 Plus with
# the Rockchip 3588 System on Chip (SOC) Running Joshua Riek's
# Ubuntu Distro for RockChip Devices:
# https://github.com/Joshua-Riek/ubuntu-rockchip


import json
import time
import gc
import os
import logging
from rockchip_3588 import RockChipData
from influx_client import InfluxClient

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataRockChip.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')

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

        payload = json.dumps(payload)

        # write data to InfluxDB
        influxdb_write.write_influx_data(client, base_payload, payload, bucket)

        del payload, socTemp, bigCore0Temp, bigCore1Temp, \
            littleCoreTemp, centerTemp, gpuTemp, npuTemp, nvmeTemp,
        littleCoreFreq, bigCore0Freq, bigCore1Freq, cpuUtil, ramUse
        gc.collect()

        time.sleep(interval)


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']

    INTERVAL = os.environ('INTERVAL')

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client, BUCKET, TABLE, INTERVAL)


if __name__ == '__main__':
    main()
