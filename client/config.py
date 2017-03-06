import json
from configparser import ConfigParser

def settings():
    config = ConfigParser()
    config.read('./cowry.conf')
    return config
# class Settings(object):
#     """docstring for Settings."""
#
#     def __init__(self):
#         super(Settings, self).__init__()
#         self.CONFIG_PATH = "./cowry.conf"
#         config = ConfigParser()
#         config.read(self.CONFIG_PATH)
#         return config
#         # self.__dict__.update(self.getConfigFromJSON(self.CONFIG_PATH))
#
#
#     def getConfigFromJSON(self, json_file_path):
#         with open(json_file_path) as config_file:
#             config = json.load(config_file)
#         return config
