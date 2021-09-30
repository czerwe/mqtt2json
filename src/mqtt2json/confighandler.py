import yaml

config = {}

def load_config():
    global config
    with open("config.yaml", "r") as fd:
        config = yaml.safe_load(fd)

if not config:
    load_config()