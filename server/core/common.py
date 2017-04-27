from core.config import Settings
from core.syslog import Syslog
from core import utils
import redis

r = redis.StrictRedis(host=self.settings.redis.host,
                      port=int(self.settings.redis.port),
                      db=int(self.settings.redis.db))
