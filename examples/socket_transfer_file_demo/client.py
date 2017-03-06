import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# clientSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)

clientSocket.connect(server_address)

print('start send file....')
with open('to_send_file/1.jpg', 'rb') as f:
    clientSocket.sendfile(f)
    clientSocket.shutdown(socket.SHUT_RDWR)
    clientSocket.close()

print('send file finished')
