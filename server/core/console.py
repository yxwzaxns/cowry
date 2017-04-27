import threading
import subprocess, sys
from core import utils

# filename = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'core/components/cowry_admin/gunicorn_runner.py')
# print(filename)

# cmd = 'python3 {}'.format(filename)
# completed = subprocess.Popen(cmd, shell=True)
#
# class WebConsole(threading.Thread):
#     """docstring for WebConsole."""
#     def __init__(self):
#         super(WebConsole, self).__init__()
#
#     def run(self):
#         gunicorn_runner.run_app()
class WebConsole(object):
    """docstring for WebConsole."""
    def __init__(self):
        super(WebConsole, self).__init__()
        self.settings = Settings()

    @staticmethod
    def start():
        filename = utils.joinFilePath(utils.getenv('COWRY_ROOT'), 'core/components/cowry_admin/gunicorn_runner.py')
        configPath = utils.getenv('COWRY_CONFIG')
        cmd = 'python3 {} {}'.format(filename, configPath)
        completed = subprocess.Popen(cmd, shell=True)
        # sys.exit()
