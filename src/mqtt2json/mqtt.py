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
        self.logger = logging.getLogger('MqttSubscriber')
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect("mosquitto.service.consul", 1883, 60)

    def run(self):
        self.logger.info('Start looping')
        self.mqtt_client.loop_forever()
        self.logger.critical('looping Stopped')

def on_connect(client, userdata, flags, rc):
    logger = logging.getLogger('mqtt::on_connect')
    for i in config['topics']:
        logger.info(f'Subscribe to topic: {i}')
        client.subscribe(i)

def on_message(client, userdata, msg):
    logger = logging.getLogger('mqtt::on_message')
    logger.info(f'{msg.topic}')
    topic_config = config['topics'][msg.topic]

    if msg.topic not in cache:
        cache[msg.topic] = Tsdb(topic_config['type'], topic_config['name'])
    cache[msg.topic].add_value(msg.payload)
