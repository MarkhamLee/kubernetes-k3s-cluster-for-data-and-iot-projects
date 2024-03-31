# Markham Lee (C) 2023
# https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard
# methods for retrieving data from a Raspberry Pis CPU, GPU sensors, et al,
# plus utility scripts for MQTT: MQTT client and generating unique client
# IDs
import os
import sys
import uuid
import influxdb_client # noqa E402
from logging_util import logger  # noqa: E402
from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt import client as mqtt

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


class MonitoringUtilities():

    def __init__():

        pass

    @staticmethod
    def influx_client(token: str, org: str, url: str) -> object:

        # create client
        write_client = influxdb_client.InfluxDBClient(url=url,
                                                      token=token, org=org)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)

        logger.info('InfluxDB Client Created')

        return write_api

    @staticmethod
    def getClientID():

        clientID = str(uuid.uuid4())

        return clientID

    @staticmethod
    def mqttClient(clientID: str, username: str, pwd: str,
                   host: str, port: int):

        def connectionStatus(client, userdata, flags, code):

            if code == 0:
                logger.info('Connected to MQTT broker')

            else:
                logger.debug(f'connection error: {code} retrying...')

        client = mqtt.Client(clientID)
        client.username_pw_set(username=username, password=pwd)
        client.on_connect = connectionStatus

        code = client.connect(host, port)

        # this is so that the client will attempt to reconnect automatically/
        # no need to add reconnect
        # logic.
        client.loop_start()

        return client, code
