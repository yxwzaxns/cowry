from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join, abspath
import re

import OpenSSL
from OpenSSL import crypto, SSL
from OpenSSL.crypto import Error
from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import dump_certificate
from OpenSSL.crypto import dump_privatekey
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import load_privatekey

CN = '127.0.0.1'
Country = 'CN'
State = 'GX'
City = 'GL'
Organization = 'university of electronic technology'
Unit = 'guet'


CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

CERT_PATTERN = re.compile(r'(-----BEGIN CERTIFICATE-----'
                          r'\r?\n[\/+=a-zA-Z0-9\r\n]*\r?\n'
                          r'-----END CERTIFICATE-----'
                          r'\r?\n?)')
PRIVATE_KEY_PATTERN = re.compile(r'(-----BEGIN PRIVATE KEY-----'
                                 r'\r?\n[\/+=a-zA-Z0-9\r\n]*\r?\n'
                                 r'-----END PRIVATE KEY-----'
                                 r'\r?\n?)')

SSL_CERTIFICATE_ERROR = 'ssl_certificate_error'
SSL_PRIVATE_KEY_ERROR = 'ssl_private_key_error'

class APIException(Exception):
    def __init__(self, error_id, message, code=500):
        super(APIException, self).__init__(message)
        self.message = message
        self.error_id = error_id
        self.code = code

def ssl_certificate_error(message):
    raise APIException(SSL_CERTIFICATE_ERROR, message, 400)

def ssl_private_key_error(message):
    raise APIException(SSL_PRIVATE_KEY_ERROR, message, 400)


def create_self_signed_cert(cert_dir= '.'):
    C_F = join(abspath(cert_dir), CERT_FILE)
    K_F = join(abspath(cert_dir), KEY_FILE)
    if not exists(C_F) or not exists(K_F):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        cert = crypto.X509()

        cert.get_subject().C = Country
        cert.get_subject().ST =  State
        cert.get_subject().L = City
        cert.get_subject().O = Organization
        cert.get_subject().OU = Unit
        cert.get_subject().CN = CN

        cert.set_serial_number(1000)

        cert.gmtime_adj_notBefore(0)

        cert.gmtime_adj_notAfter(315360000)

        cert.set_issuer(cert.get_subject())

        cert.set_pubkey(k)

        cert.sign(k, 'sha1')

        with open(C_F, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(K_F, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def validate_ssl_cert(certificate, private_key):
    def gen_message(e):
        if isinstance(e, Error):
            msg = ''.join([' '.join(m) for m in e.message])
        else:
            msg = e.message

        return msg or "load pem file failed"

    certs = CERT_PATTERN.findall(certificate)
    if not certs:
        raise ssl_certificate_error("SSL certificate is invalid: %s." % "no certificate found")
    priv_keys = PRIVATE_KEY_PATTERN.findall(private_key)
    if not priv_keys:
        raise ssl_private_key_error("SSL private key is invalid: %s." % "no private key found")

    def _load_certificate(cert_data):
        try:
            return load_certificate(FILETYPE_PEM, cert_data)
        except Exception as e:
            msg = gen_message(e)
            LOG.error("validate ssl certs failed: %s.", msg)
            raise ssl_certificate_error("SSL certificate is invalid: %s." % msg)

    def _load_private_key(private_key_data):
        try:
            return load_privatekey(FILETYPE_PEM, private_key_data)
        except Exception as e:
            msg = gen_message(e)
            LOG.error("validate ssl private key failed: %s.", msg)
            raise ssl_private_key_error("SSL private key is invalid: %s." % msg)

    # check first part to ensure pem file is loadable
    crt = _load_certificate(certs[0])
    key = _load_private_key(priv_keys[0])

    crt_chain = [_load_certificate(c) for c in certs]
    key_chain = [_load_private_key(p) for p in priv_keys]

    try:
        ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        ctx.use_privatekey(key)
        ctx.use_certificate(crt)
        ctx.check_privatekey()
    except Exception as e:
        message = gen_message(e)
        LOG.error("https pem files key pair is not matched: %s.", message)
        raise ssl_certificate_error("SSL key pair is not matched: %s." % message)

    crt_chain_data = b''.join([dump_certificate(FILETYPE_PEM, cc) for cc in crt_chain])
    key_chain_data = b''.join([dump_privatekey(FILETYPE_PEM, kc) for kc in key_chain])
    return crt_chain_data, key_chain_data

create_self_signed_cert()
with open(CERT_FILE, 'r') as f:
    cert = f.read()
with open(KEY_FILE, 'r') as f:
    key = f.read()
print(cert,key)
print(validate_ssl_cert(cert, key))
