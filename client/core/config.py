from configparser import ConfigParser

class Settings(ConfigParser):
    """docstring for Settings."""
    def __init__(self, configPath= None):
        super(Settings, self).__init__()
        if configPath is None:
            self.configurePath = "cowry.conf"
        else:
            self.configurePath =  configPath
        self.read(self.configurePath)

        self.analysis()

    def analysis(self):
        sections = [x.lower() for x in self.keys()]
        confDict = {str(x.lower()): {str(y.lower()): self[x][y] for y in list(self[x].keys()) if y not in self.defaults().keys()} for x in list(self.keys())}
        confDict['default'] = dict(self.defaults())
        self.map(**confDict)

    # this is a very bad function, there must ba a better way to convert object from deep dictionary
    def map(self, **entries):
        for key, value in entries.items():
            value2 = (Struct(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2

class Struct:
    def __init__(self, **entries):
        for key, value in entries.items():
            value2 = (Struct(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2
