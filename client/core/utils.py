import os
import hashlib
import random
import uuid
import time
import shutil
import re
import socket
from ast import literal_eval
import _thread
import OpenSSL
import requests

def prettySize(num, suffix='B'):
    num = int(num)
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "{:.3f} {}{}".format(num, unit, suffix)
        num /= 1024.0

def getSizeByPath(filepath):
    return os.path.getsize(filepath)

def getBaseNameByPath(filepath):
    return os.path.basename(filepath)

def calculateHashCodeForFile(filepath):
    try:
        with open(filepath, 'rb') as f:
            fileHashCode = hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return (1, str(e))
    return fileHashCode

def calculateHashCodeForString(string, method='md5'):
    """pass."""
    return getattr(hashlib, method)(string.encode('utf8')).hexdigest()

def check_public_key(key):
    # key = base64.b64decode(line.strip().split()[1].encode('ascii'))
    # fp_plain = hashlib.md5(key).hexdigest()
    return True

def generateSaltCipher(key):
    key = key.encode() + os.urandom(32)
    return hashlib.sha256(key).hexdigest()[0:32]

def generateRandomDigitFromRange(start, end):
    return random.randrange(start, end)

def rebuildDictFromBytes(bytestring):
    return literal_eval(bytestring.decode('utf8'))

def startNewThread(work, params=()):
    if params:
        _thread.start_new_thread(work, params)
    else:
        _thread.start_new_thread(work, ())

def generateAuthToken():
    return uuid.uuid4().hex.upper()

def getCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def joinFilePath(*params):
    params = [x for x in params]
    return os.path.join(*params)

def deleteFile(filepath):
    os.remove(filepath)

def getenv(name):
    return os.getenv(name)

def setenv(name, value):
    os.environ[name] = str(value)

def getCwd():
    """pass."""
    return os.getcwd()

def copyfile(src, dst):
    """pass."""
    try:
        shutil.copyfile(src, dst)
    except Exception as e:
        return (1, str(e))
    else:
        return (0, 'ok')

def delfolder(folderpath):
    shutil.rmtree(folderpath)

def delFilesFromFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            return False
    return True

def checkFolderExists(path):
    """pass."""
    return os.path.isdir(path)

def checkFileExists(filepath):
    return os.path.isfile(filepath)

def checkAbsPath(path):
    """pass."""
    return os.path.isabs(path)

def makeDirs(filepath):
    """pass."""
    return os.makedirs(filepath)

def verifyDomain(domain):
    reg = r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
    return re.search(reg, domain)

def getHostAddr():
    return socket.gethostbyname(socket.gethostname())
# client functions
def getUserHome():
    return os.path.expanduser('~')

def convertPathFromHome(path):
    return os.path.expanduser(path)

def moveFile(src, dst):
    shutil.move(src, dst)

def importCert(path):
    return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, path)

def getCertInfo(path):
    filehash = calculateHashCodeForFile(path)
    with open(path, 'r') as f:
        certfile = f.read()
    cert = importCert(certfile)
    cert_digest = cert.digest("sha256")
    cert_info = {'digest': cert_digest.decode(),
                 'filehash': filehash}
    return cert_info

def verify_cert(path, api_path):
    cert_info = getCertInfo(path)
    ret = requests.get('http://{}:3000/api/certs'.format(api_path))
    if rebuildDictFromBytes(ret.content)['cert_digest_sha256'] == cert_info['digest']:
        return True
    else:
        return False
