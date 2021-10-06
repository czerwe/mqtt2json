import logging
import os

from flask import Flask, jsonify, request
from pprint import pprint
import json
import yaml
import os
import time
from .grafana import GrafanaRequest
from .mqtt import MqttSubscriber
import mqtt2json.confighandler
from .cache import cache
from .confighandler import config
from .aggregators import Aggregator

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

b = os.listdir(".")
thread = MqttSubscriber()
thread.start()

methods = ("GET", "POST")


@app.route("/")
def root():
    return jsonify({"status": "ok"})


@app.route("/search", methods=methods)
def search():
    # req = GrafanaRequest(request.data)
    retval = [cache[i].name for i in cache] + [ key for key in config.get('aggregator', {}).keys()]
    return jsonify(retval)


@app.route("/query", methods=['POST'])
def query():
    logger = logging.getLogger('query')
    req = GrafanaRequest(request.data)
    # pprint(req)
    retval = []

    for item in cache:
        if cache[item].name in req.targets():
            retval.append(cache[item].datapoint(req.start, req.stop))
            logger.info(f'Return Target "{retval[-1]["target"]}" with {len(retval[-1]["datapoints"])} items')

    for akey in [akey for akey in config.get('aggregator', {}).keys() if akey in req.targets()]:
        aggr = Aggregator(akey, config['aggregator'][akey])
        retval.append(aggr.target(req.start, req.stop))

    # pprint(cache)
    # print('-----------------')
    # pprint(retval)
    # print('-----------------')
    return jsonify(retval)

