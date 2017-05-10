import os, re
import sys

import gunicorn.app.base
import gunicorn.glogging
import gunicorn.workers.ggevent
from gunicorn.app.wsgiapp import run


PROJECT_PATH = os.path.dirname(sys.argv[1])
os.sys.path.append(PROJECT_PATH)

from core import utils
utils.setenv('COWRY_CONFIG', sys.argv[1])
utils.setenv('COWRY_ROOT', PROJECT_PATH)

from core.config import Settings
settings = Settings()

ERROR_LOG = utils.joinFilePath(PROJECT_PATH, 'log/error.log')
ACCESS_LOG = utils.joinFilePath(PROJECT_PATH, 'log/access.log')

HOST = settings.webconsole.host
PORT = settings.webconsole.port

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

# def run_app():
#     options = {
#         'worker-class': "gevent",
#         'bind': '{}:{}'.format(HOST, PORT),
#         'workers': '1',
#         'max-requests': "5000",
#         "max-requests-jitter": "5000",
#         "access-logfile": "{}".format(ACCESS_LOG),
#         "error-logfile": "{}".format(ERROR_LOG),
#     }
#     StandaloneApplication(app, options).run()

    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv[0] = 'gunicorn'
    del sys.argv[1]
    if settings.default.debug == 'True':
        sys.argv += ["-k", "gevent", "-w", "1",
                     "--max-requests", "5000", "--max-requests-jitter", "5000",
                     "--access-logfile", "-",
                     "--error-logfile", "-",
                     '-b', '{}:{}'.format(HOST, PORT), 'cowry_admin:app']
    else:
        sys.argv += ["-k", "gevent", "-w", "1",
                     "--max-requests", "5000", "--max-requests-jitter", "5000",
                     "--access-logfile", "{}".format(ACCESS_LOG),
                     "--error-logfile", "{}".format(ERROR_LOG),
                     '-b', '{}:{}'.format(HOST, PORT), 'cowry_admin:app']

    # print(sys.argv)
    sys.exit(run())

if __name__ == "__main__":
    run_app()
