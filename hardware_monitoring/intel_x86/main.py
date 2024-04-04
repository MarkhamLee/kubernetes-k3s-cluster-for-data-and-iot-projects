#!/usr/bin/env python
# Markham Lee (C) 2023
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor the CPU and NVME temperatures on Intel x86 Nodes
# only monitoring temps with this for now as the Prometheus stack
# handles the rest: compute, disk space, ram, etc.


import gc
import logging
import os
from time import sleep
from sys import stdout
from intel_x86 import Intelx86
from influxdb_client import Point

# set up/configure logging with stdout so it can be picked up by K8s
logger = logging.getLogger('intel_telemetry_logger')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')  # noqa: E501
handler.setFormatter(formatter)
logger.addHandler(handler)


def monitor(client: object, get_data: object, BUCKET: str, ORG: str,
            TABLE: str, INTERVAL: int):

    while True:

        # get CPU, GPU and NVME temperatures
        core_temp, nvme_temp = get_data.getTemps()

        point = (
            Point(TABLE)
            .tag("cluster_nodes", "node temps")
            .field("nvme_temp", nvme_temp)
            .field("core_temp", core_temp)
        )

        client.write(bucket=BUCKET, org=ORG, record=point)

        del nvme_temp, core_temp
        gc.collect()

        sleep(INTERVAL)


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']
    INTERVAL = os.environ['INTERVAL']

    # instantiate utilities class
    device_data = Intelx86()

    # get client
    client = device_data.influx_client(TOKEN, ORG, URL)

    monitor(client, device_data, BUCKET, ORG, TABLE, INTERVAL)


if __name__ == '__main__':
    main()
