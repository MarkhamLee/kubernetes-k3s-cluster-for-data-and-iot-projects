# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/k3s-data-platform-IoT
# Script to monitor temperatures of the AMD 5560u on the
# Beelink SER5s that are being used for the cluster nodes.
# Only monitoring the temps (for now), because I'm using the
# kube-prometheus stack to monitor CPU load, disk space, RAM, etc.

import gc
import os
import sys
from time import sleep
from amd_5560u import AMD5560Data

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


def monitor(client: object, get_data: object, BUCKET: str, ORG: str,
            TABLE: str, DEVICE_ID: str, INTERVAL: str):

    logger.info(f'Starting HW monitoring for {DEVICE_ID}')

    while True:

        # get CPU, GPU and NVME temperatures
        nvme_temp, cpu_temp, amd_gpu_temp = get_data.amd_linux_data()

        # get base_payload
        base_payload = get_base_payload()

        payload = {
            "nvme_temp": nvme_temp,
            "cpu_temp": cpu_temp,
            "amd_gpu_temp": amd_gpu_temp
        }

        # write data to InfluxDB
        influxdb_write.write_influx_data(client, base_payload, payload, BUCKET)

        del nvme_temp, cpu_temp, amd_gpu_temp, payload, base_payload
        gc.collect()
        sleep(INTERVAL)


def main():

    DEVICE_ID = os.environ['DEVICE_ID']
    INTERVAL = int(os.environ['INTERVAL'])
    TOKEN = os.environ['TOKEN']
    ORG = os.environ['ORG']
    URL = os.environ['URL']
    BUCKET = os.environ['BUCKET']
    TABLE = os.environ['TABLE']

    # instantiate utilities class
    device_data = AMD5560Data()

    # get client
    client = influxdb_write.influx_client(TOKEN, ORG, URL)

    monitor(client, device_data, BUCKET, ORG, TABLE, DEVICE_ID, INTERVAL)


if __name__ == '__main__':
    main()
