"""
Code example for publishing data to the Brewblox eventbus on a fixed schedule

Dependencies:
- paho-mqtt
- schedule
"""

import json
from random import random
from ssl import CERT_NONE
from time import sleep

import schedule
from paho.mqtt import client as mqtt

# 172.17.0.1 is the default IP address for the host running the Docker container
# Change this value if Brewblox is installed on a different computer
HOST = '172.17.0.1'

# This is a constant value. You never need to change it.
TOPIC = 'brewcast/history'

# Create a websocket MQTT client
client = mqtt.Client(transport='websockets')
client.ws_set_options(path='/eventbus')
client.tls_set(cert_reqs=CERT_NONE)
client.tls_insecure_set(True)


def publish():

    try:
        client.connect(host=HOST, port=443)
        client.loop_start()

        # https://brewblox.netlify.app/dev/reference/event_logging.html
        value = 20 + ((random() - 0.5) * 10)
        message = {
            'key': 'scheduledscript',
            'data': {'value[degC]': value}
        }

        client.publish(TOPIC, json.dumps(message))
        print(f'sent {message}')

    finally:
        client.loop_stop()


# For more examples on how to schedule tasks, see:
# https://github.com/dbader/schedule
schedule.every().minute.at(':05').do(publish)

while True:
    schedule.run_pending()
    sleep(1)