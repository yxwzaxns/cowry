import socket
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# clientSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)

clientSocket.connect(server_address)

print('start send file....')
filePath = "to_send_file/1.jpg"
fileSize = os.path.getsize(filePath)
sizeInfo = b''.join((str.encode(str(fileSize)), b' '*(1024 - len(str(fileSize)))))
print('sizeInfo is : {}'.format(len(sizeInfo)))
clientSocket.send(sizeInfo)

with open(filePath, 'rb') as f:
    clientSocket.sendfile(f)
# extendInfo = b''.join((b' '*(1024 - fileSize % 1024 - 3), b'EOF'))
    # clientSocket.shutdown(socket.SHUT_RDWR)
# print('senf extend info to end : {}'.format(extendInfo))
# clientSocket.send(extendInfo)
print('send file finished')
info = clientSocket.recv(1).strip()
while True:
    if info == b'0':
        print('recv info end')
        break
    else:
        print(info)
    info = clientSocket.recv(1).strip()
    if len(info) == 0:
        break
