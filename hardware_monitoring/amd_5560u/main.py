#!/usr/bin/env python
# Markham Lee (C) 2023
# K3s Data Platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor temperatures of the AMD 5560u on the
# Beelink SER5s that are being used for the cluster nodes.
# Only monitoring the temps (for now), because I'm using the
# kube-prometheus stack to monitor CPU load, disk space, RAM,
# etc.

import time
import gc
import logging
import os
from amd_5560u import AMD5560Data
from influxdb_client import Point

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataLinuxCPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client: object, get_data: object, BUCKET: str, ORG: str,
            TABLE: str):

    while True:

        time.sleep(5)

        # get CPU, GPU and NVME temperatures
        nvme_temp, cpu_temp, amdgpu_temp = get_data.amd_linux_data()

        point = (
            Point(TABLE)
            .tag("cluster_nodes", "node temps")
            .field("nvme_temp", nvme_temp)
            .field("cpu_temp", cpu_temp)
            .field("amdgpu_temp", amdgpu_temp)
        )

        client.write(bucket=BUCKET, org=ORG, record=point)

        del nvme_temp, cpu_temp, amdgpu_temp
        gc.collect()


def main():

    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']

    # instantiate utilities class
    device_data = AMD5560Data()

    # get client
    client = device_data.influx_client(TOKEN, ORG, URL)

    monitor(client, device_data, BUCKET, ORG, TABLE)


if __name__ == '__main__':
    main()
