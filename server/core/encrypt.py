import OpenSSL
from OpenSSL import crypto, SSL
from OpenSSL.crypto import Error
from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import dump_certificate
from OpenSSL.crypto import dump_privatekey
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import load_privatekey

import re
from os.path import exists, join, abspath
from core.syslog import Syslog
from core.config import Settings
from core.utils import *


CERT_PATTERN = re.compile(r'(-----BEGIN CERTIFICATE-----'
                          r'\r?\n[\/+=a-zA-Z0-9\r\n]*\r?\n'
                          r'-----END CERTIFICATE-----'
                          r'\r?\n?)')
PRIVATE_KEY_PATTERN = re.compile(r'(-----BEGIN PRIVATE KEY-----'
                                 r'\r?\n[\/+=a-zA-Z0-9\r\n]*\r?\n'
                                 r'-----END PRIVATE KEY-----'
                                 r'\r?\n?)')

class SSLCertSetting(object):
    """docstring for SSLCertSetting."""
    def __init__(self):
        super(SSLCertSetting, self).__init__()
        self.log = Syslog()
        self.settings = Settings()

    def create_self_signed_cert(self, common_name):
        C_F = self.settings.certificates.certificate
        K_F = self.settings.certificates.privatekey
        P_F = joinFilePath(getDirNameByPath(self.settings.certificates.privatekey),
                                 'server.pub.key')

        if not exists(C_F) or not exists(K_F):
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()

        cert.get_subject().C = self.settings.certificates.country
        cert.get_subject().ST =  self.settings.certificates.state
        cert.get_subject().L = self.settings.certificates.city
        cert.get_subject().O = self.settings.certificates.organization
        cert.get_subject().OU = self.settings.certificates.unit
        cert.get_subject().CN = common_name

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

        with open(P_F, "wb") as f:
            f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, k))

    def validate_ssl_cert(self):
        certificate = getFileContent(self.settings.certificates.certificate)
        privatekey = getFileContent(self.settings.certificates.privatekey)
        certs = CERT_PATTERN.findall(certificate)
        if not certs:
            self.log.error("SSL certificate is invalid: no certificate found {}".format(self.settings.certificates.certificate))
            exit()
        priv_keys = PRIVATE_KEY_PATTERN.findall(privatekey)
        if not priv_keys:
            self.log.error("SSL private key is invalid: no private key found {}".format(self.settings.certificates.privatekey))
            exit()

        def _load_certificate(cert_data):
            try:
                return load_certificate(FILETYPE_PEM, cert_data)
            except Exception as e:
                self.log.error("validate ssl certs failed: {}.".format(e))
                exit()

        def _load_private_key(private_key_data):
            try:
                return load_privatekey(FILETYPE_PEM, private_key_data)
            except Exception as e:
                self.log.error("validate ssl private key failed: {}".format(e))
                exit()

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
            self.log.error("cert pem files key pair is not matched: {}.".format(e))
            exit()

        crt_chain_data = b''.join([dump_certificate(FILETYPE_PEM, cc) for cc in crt_chain])
        key_chain_data = b''.join([dump_privatekey(FILETYPE_PEM, kc) for kc in key_chain])
        return crt_chain_data, key_chain_data
