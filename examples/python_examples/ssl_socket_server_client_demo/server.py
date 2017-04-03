import socket, ssl

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")

ssl_sock = context.wrap_socket(serverSocket, server_hostname='127.0.0.1')

ssl_sock.bind(('127.0.0.1', 10023))
ssl_sock.listen(5)

client, address = ssl_sock.accept()
while True:
    info = client.recv(10)
    if info == b'':
        client.close()
        break
    print(info)
