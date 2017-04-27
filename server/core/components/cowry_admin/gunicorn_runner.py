import os, re
import sys

import gunicorn.app.base
import gunicorn.glogging
import gunicorn.workers.ggevent
from gunicorn.app.wsgiapp import run

import utils

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

ERROR_LOG = utils.joinFilePath(PROJECT_PATH, 'log/error.log')
ACCESS_LOG = utils.joinFilePath(PROJECT_PATH, 'log/access.log')

HOST = '0.0.0.0'
PORT = '8000'

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

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv += ["-k", "gevent", "-w", "1",
                 "--max-requests", "5000", "--max-requests-jitter", "5000",
                 "--access-logfile", "{}".format(ACCESS_LOG),
                 "--error-logfile", "{}".format(ERROR_LOG),
                 '-b', '{}:{}'.format(HOST, PORT), 'cowry_admin:app']

    sys.exit(run())

if __name__ == "__main__":
    run_app()
