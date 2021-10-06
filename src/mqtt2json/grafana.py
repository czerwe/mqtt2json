import json
import logging
from datetime import datetime
import pytz
from dateutil import parser

class GrafanaRequest(object):

    def __init__(self, data):
        super(GrafanaRequest, self).__init__()
        self.logger = logging.getLogger('GrafanaRequest')
        try:
            self._data = json.loads(data.decode("utf-8"))
        except Exception as e:
            self.logger.warning(f'Failed to jsonify request: {e}')
            self.logger.debug(data)
        else:
            startString = self._data.get('range', {}).get('from', None)
            if startString:
                self._start = parser.parse(startString)
            stopString = self._data.get('range', {}).get('to', None)
            if stopString:
                self._stop = parser.parse(stopString)

            self.logger.debug(f"{startString} - {stopString}")

            self._targets = self._data.get('targets', [])

    def targets(self):
        return [target["target"] for target in self._targets]


    @property
    def start(self):
        self.logger.warning(self._start)
        # self.logger.critical(self._start.timestamp())
        return self._start.timestamp() * 1000


    @property
    def stop(self):
        return self._stop.timestamp() * 1000