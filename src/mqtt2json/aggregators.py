import logging

from .cache import cache

class Aggregator(object):

    def __init__(self, name, aggr):
        super(Aggregator, self).__init__()
        self.logger = logging.getLogger(f'aggregator::{name}')
        self._name = name
        self._config = aggr
        self._tsdbs = [cache[topic] for topic in cache if cache[topic].name in self._config['metrics']]

    def target(self, start, end ):
        if self._config['type'] == 'min':
            datapoints = [tsdb.latest(start, end) for tsdb in self._tsdbs]

        datapoints = sorted(datapoints, key=lambda a: a[0])[0]
        return {'target': self._name, "datapoints": datapoints}



