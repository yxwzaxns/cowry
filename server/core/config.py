from configparser import ConfigParser
from core import utils


class Settings(ConfigParser):
    """docstring for Settings."""
    def __init__(self):
        super(Settings, self).__init__()
        self.configurePath =  utils.getenv('COWRY_CONFIG') or 'cowry.conf'
        self.read(self.configurePath)

        self.analysis()

    def autosave(func):
        def wrapper(self, conf):
            func(self, conf)
            with open(self.configurePath, 'w') as f:
                self.write(f)
            self.analysis()
        return wrapper

    def analysis(self):
        confDict = {str(x.lower()): {str(y.lower()): self[x][y] for y in list(self[x].keys()) if y not in self.defaults().keys()} for x in list(self.keys())}
        confDict['default'] = dict(self.defaults())
        self.map(**confDict)

    # this is a very bad function, there must ba a better way to convert object from deep dictionary
    def map(self, **entries):
        for key, value in entries.items():
            value2 = (Struct(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2

    @autosave
    def _set(self, conf):
        self.set(str(conf[0].upper()), str(conf[1]), str(conf[2]))

class Struct:
    def __init__(self, **entries):
        for key, value in entries.items():
            value2 = (Struct(**value) if isinstance(value, dict) else value)
            self.__dict__[key] = value2
