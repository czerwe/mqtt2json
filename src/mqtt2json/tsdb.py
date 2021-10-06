import json
import logging
from datetime import datetime
from pprint import pprint

class Tsdb(object):
    def __init__(self, mtype: str, mname: str):
        super(Tsdb, self).__init__()

        self._type = mtype
        self._name = mname
        self.logger = logging.getLogger(f'tsdb::{self.name}')

        self._value = []

    def __len__(self):
        return len(self._value)

    @property
    def name(self):
        return f'{self._name}_{self._type}'

    def add_value(self, json_payload):
        self.logger.info(f'got payload')
        payload = json.loads(json_payload)
        self._value.append([payload["val"], payload['ts']])

    def latest(self, start, end):
        existing_datapoints = self.datapoint(start, end)['datapoints']

        retval = existing_datapoints[-1] if len(existing_datapoints) else []
        return retval
        return self.datapoint(start, end)['datapoints']

    def datapoint(self, start, end ):
        self.logger.info(f'start: {start}')
        self.logger.info(f'end: {end}')
        datapoints = [datapoint for datapoint in self._value if datapoint[1] >= start and datapoint[1] <= end]


        # for d in self._value:
        #     print(d[1])
        retVal = {'target': self.name, "datapoints": datapoints}
        return retVal
