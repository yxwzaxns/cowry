"""functions helper."""

from ast import literal_eval
import os
import hashlib
import random
import uuid
import time
import shutil
import re
import socket
import _thread


def addAppPath(path):
    """Add a path to sys path."""
    os.sys.path.append(path)

def getCwd():
    """pass."""
    return os.getcwd()

def checkAbsPath(path):
    """pass."""
    return os.path.isabs(path)

def prettySize(num, suffix='B'):
    """pass."""
    num = int(num)
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "{:.3f} {}{}".format(num, unit, suffix)
        num /= 1024.0

def getSizeByPath(filepath):
    """pass."""
    return os.path.getsize(filepath)

def getBaseNameByPath(filepath):
    """pass."""
    return os.path.basename(filepath)

def getDirNameByPath(filepath):
    """pass."""
    return os.path.dirname(filepath)

def calculateHashCodeForFile(filepath):
    """pass."""
    try:
        with open(filepath, 'rb') as f:
            fileHashCode = hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return (1, str(e))
    return fileHashCode
def calculateHashCodeForString(string, method='md5'):
    """pass."""
    return getattr(hashlib, method)(string.encode('utf8')).hexdigest()
    # return hashlib.md5(str.encode('utf8')).hexdigest()

def generateRandomDigitFromRange(start, end):
    """pass."""
    return random.randrange(start, end)

def rebuildDictFromBytes(bytestr):
    """pass."""
    return literal_eval(bytestr.decode('utf8'))

def startNewThread(work, params=()):
    """pass."""
    if params:
        _thread.start_new_thread(work, params)
    else:
        _thread.start_new_thread(work, ())

def seperateFileName(filename):
    """pass."""
    return  os.path.splitext(filename)

def getFileContent(filepath, method= ''):
    """pass."""
    mode = 'r{}'.format(method)
    with open(filepath, mode) as f:
        content = f.read()
    return content

def generateAuthToken():
    """pass."""
    return uuid.uuid4().hex.upper()

def getCurrentTime():
    """pass."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def joinFilePath(*params):
    """pass."""
    params = [x for x in params]
    return os.path.join(*params)

def deleteFile(filepath):
    """pass."""
    try:
        os.remove(filepath)
    except Exception as e:
        return (1, str(e))
    else:
        return (0, 'ok')

def copyfile(src, dst):
    """pass."""
    try:
        shutil.copyfile(src, dst)
    except Exception as e:
        return (1, str(e))
    else:
        return (0, 'ok')

def getenv(name):
    """pass."""
    return os.getenv(name)

def setenv(name, value):
    """pass."""
    os.environ[name] = str(value)

def makeDirs(filepath):
    """pass."""
    return os.makedirs(filepath)

def delfolder(folderpath):
    """pass."""
    shutil.rmtree(folderpath)

def checkFileExists(filepath):
    """pass."""
    return os.path.isfile(filepath)

def checkFolderExists(path):
    """pass."""
    return os.path.isdir(path)

def verifyDomain(domain):
    """pass."""
    reg = r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
    return re.search(reg, domain)

def getHostAddr():
    """pass."""
    return socket.gethostbyname(socket.gethostname())
