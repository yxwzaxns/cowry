import json

class Settings(object):
    """docstring for Settings."""
    CONFIG_PATH = "./config.json"

    def __init__(self):
        super(Settings, self).__init__()
        self.__dict__.update(self.getConfigFromJSON(self.CONFIG_PATH))


    def getConfigFromJSON(self, json_file_path):
        with open(json_file_path) as config_file:
            config = json.load(config_file)
        return config
