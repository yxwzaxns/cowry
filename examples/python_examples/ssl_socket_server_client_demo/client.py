import socket
import ssl


sslContext = ssl.create_default_context()
sslContext.load_verify_locations('certs/server.crt')

tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctrlSock = sslContext.wrap_socket(tmpSock, server_hostname='127.0.0.1')
ctrlSock.connect(('127.0.0.1', 10023))
# print(ssl.get_server_certificate(('127.0.0.1', 10023)))
while True:
    ctrlSock.send(str.encode(input()))
