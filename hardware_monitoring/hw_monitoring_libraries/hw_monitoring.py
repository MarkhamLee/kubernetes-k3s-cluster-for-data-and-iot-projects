# Markham Lee (C) 2023 - 2024
# kubernetes-k3s-data-and-IoT-platform
# https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-Platform
# Utility methods for monitoring hardware/nodes within the K3s cluster;
# primarily used for extended/supplemental monitoring beyond what's
# possible via the typical K8s HW monitoring tools. E.g., monitoring
# GPU temps for single board computers.
import os
import sys
import uuid
from paho.mqtt import client as mqtt

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hw_monitoring_libraries.logging_util import logger  # noqa: E402


class MonitoringUtilities():

    def __init__(self):

        pass

    # generate unique client IDs for connecting to the MQTT broker
    @staticmethod
    def getClientID():

        clientID = str(uuid.uuid4())

        return clientID

    # Generate MQTT client
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
