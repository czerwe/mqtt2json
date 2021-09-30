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
    # print('SEARCH')
    req = GrafanaRequest(request.data)
    retval = [cache[i].name for i in cache]
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
    # pprint(retval)
    return jsonify(retval)

