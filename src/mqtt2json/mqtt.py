import paho.mqtt.client as mqtt
import json
from .confighandler import config
from .cache import cache
# mqtt_client = None
from .tsdb import Tsdb
import threading
import logging

class MqttSubscriber(threading.Thread):

    def __init__(self):
        super(MqttSubscriber, self).__init__(daemon=False)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect("mosquitto.service.consul", 1883, 60)

    def run(self):
        self.mqtt_client.loop_forever()

def on_connect(client, userdata, flags, rc):
    for i in config['topics']:
        client.subscribe(i)

def on_message(client, userdata, msg):
    logger = logging.getLogger('mqtt::msg')
    logger.info(f'{msg.topic}')
    topic_config = config['topics'][msg.topic]

    if msg.topic not in cache:
        cache[msg.topic] = Tsdb(topic_config['type'], topic_config['name'])
    cache[msg.topic].add_value(msg.payload)
