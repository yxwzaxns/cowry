"""Encrypt files ations."""
import random
import os
import base64
import struct
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from core.syslog import Syslog
from core import utils

AES_CBC = "aes_cbc"
DES_CBC = ""

C_TYPE = {
    "AES-128-CBC": {
        "C_L": 16,
        "F": AES_CBC
    },
    "DES-128-CBC": {
        "C_L": 16,
        "F": DES_CBC
    }
}

class Cryptogram(object):
    """docstring for Cryptogram."""

    def __init__(self):
        super(Cryptogram, self).__init__()
        self.log = Syslog()

    def encrypt_text(self, string, key, mode='AES-128-CBC'):
        CKey = self.convertKey(string, mode)
        rsa_key = RSA.importKey(key)
        c = rsa_key.encrypt(CKey.encode(), 'a')
        cb64 = base64.b64encode(c[0])
        return (0, cb64)

    def decrypt_text(self, string, key):
        rsa_key = RSA.importKey(key)
        c = base64.b64decode(string)
        p = rsa_key.decrypt(c).decode()
        return (0, p)

    def encrypt(self, key, filepath, mode='AES-128-CBC'):
        self.log.info('prepare encrypt file : {} \nuse mode is :{} \n, Cipher is :{} '.format(filepath, mode, key))
        try:
            encrypt_with_mode = getattr(self, 'encrypt_file_with_' + C_TYPE[mode]['F'])
        except Exception as e:
            raise
        else:
            CKey = self.convertKey(key, mode)
            # CKey = key
            return encrypt_with_mode(CKey, filepath)

    def decrypt(self, key, filepath, savefilepath, nck=0, mode='AES-128-CBC'):
        self.log.info('prepare decrypt file : {} \nuse mode is :{} \n, Cipher is :{} '.format(filepath, mode, key))
        try:
            decrypt_with_mode = getattr(self, 'decrypt_file_with_' + C_TYPE[mode]['F'])
        except Exception as e:
            raise
        else:
            if nck == 0:
                CKey = self.convertKey(key, mode)
            else:
                CKey = key
            self.log.info(CKey)
            # CKey = key
            return decrypt_with_mode(CKey, filepath, out_filename=savefilepath)

    def convertKey(self, key, mode):
        cipherLength = C_TYPE[mode]['C_L']
        # 128
        hashcode = hashlib.sha512(str.encode(key)).hexdigest()
        newKey = hashcode[0:cipherLength]
        return newKey

    @staticmethod
    def encrypt_file_with_aes_cbc(key, in_filename, out_filename=None, chunksize=64*1024):
        # """Encrypts a file using AES (CBC mode) with the
        #     given key.
        #
        #     key:
        #         The encryption key - a string that must be
        #         either 16, 24 or 32 bytes long. Longer keys
        #         are more secure.
        #
        #     in_filename:
        #         Name of the input file
        #
        #     out_filename:
        #         If None, '<in_filename>.enc' will be used.
        #
        #     chunksize:
        #         Sets the size of the chunk which the function
        #         uses to read and encrypt the file. Larger chunk
        #         sizes can be faster for some files and machines.
        #         chunksize must be divisible by 16.
        # """
        if not out_filename:
            baseName = os.path.basename(in_filename)
            out_filename = '/tmp/' + baseName + '.enc'

        # iv = os.urandom(16)
        iv = b'0000000000000000'
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        enc_filepath = os.path.abspath(out_filename)
        return (0, enc_filepath)

    @staticmethod
    def decrypt_file_with_aes_cbc(key, in_filename, out_filename=None, chunksize=24*1024):
        # """ Decrypts a file using AES (CBC mode) with the
        #     given key. Parameters are similar to encrypt_file,
        #     with one difference: out_filename, if not supplied
        #     will be in_filename without its last extension
        #     (i.e. if in_filename is 'aaa.zip.enc' then
        #     out_filename will be 'aaa.zip')
        # """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    try:
                        outfile.write(decryptor.decrypt(chunk))
                    except Exception as e:
                        return (1, str(e))

                outfile.truncate(origsize)
        # dec_filepath = os.path.abspath(out_filename)
        return (0, "ok")
