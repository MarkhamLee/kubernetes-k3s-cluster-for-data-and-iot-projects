import os
import requests
import sys
from influxdb_client import InfluxDBClient # noqa E402
from influxdb_client.client.write_api import SYNCHRONOUS # noqa E402

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from network_monitoring_libraries.\
    logging_utils import console_logging  # noqa: E402

logger = console_logging('Network_utils')


def send_slack_webhook(webhook_url: str, message: str):

    headers = {
        'Content-type': 'application/json'

    }

    payload = {
        "text": message
    }

    response = requests.post(webhook_url, headers=headers, json=payload)

    code = response.status_code

    if code != 200:
        logger.warning('Publishing of alert to Slack webhook failed with response code: %s',  # noqa: E501
                       code)  # noqa: E501

    else:

        logger.info('Publishing of alert to Slack webhook succeeded with code: %s',  # noqa: E501
                    code)

    return code


def create_influx_client(token, org, url):

    # create client
    write_client = InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    return write_api


# Takes an input payload and appends it to a JSON with that payload's
# InfluxDB table and tag data, and then writes the combined
def write_influx_data(client: object, base: dict, data: dict, BUCKET: str):

    # combine the baseline payload with the data to be written to InfluxDB
    base.update({"fields": data})

    # write data to InfluxDB
    client.write(bucket=BUCKET, record=base)


def write_data(base_payload: dict,
               data: dict,
               client: object,
               bucket: str,
               data_message: str,
               slack_webhook: str):

    # note: create payload with "types" defined before sending
    # data

    # combine the baseline payload with the data to be written to InfluxDB
    base_payload.update({"fields": data})

    try:
        # write data to InfluxDB
        client.write(bucket=bucket,
                     record=base_payload)
        logger.info('Technitium data was successfully written to InfluxDB')  # noqa: E501

    except Exception as e:
        message = (f'InfluxDB write failed with error: {e}')
        logger.warning(message)
        response = send_slack_webhook(slack_webhook, message)
        logger.info('InfluxDB write failure alert sent with code: %s',
                    response)  # noqa: E501
        return response


def send_uptime_kuma_heartbeat(uptime_kuma_webhook, id):

    try:
        requests.get(uptime_kuma_webhook)

    except Exception as e:
        logger.warning('Publishing of Uptime Kuma alert for ID %s failed with error: %s',  # noqa: E501
                       id,
                       e)  # noqa: E501
