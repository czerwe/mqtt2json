import yaml
import os

config = {}

def load_config():
    global config
    config_file = os.environ.get('CONFIGFILE', 'config.yaml')

    with open(config_file, "r") as fd:
        config = yaml.safe_load(fd)

if not config:
    load_config()