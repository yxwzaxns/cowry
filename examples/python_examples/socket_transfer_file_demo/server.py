import socket, os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# serverSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)

serverSocket.bind(server_address)

serverSocket.listen(5)

(clientSocket, clientAddress) = serverSocket.accept()

print(clientAddress)
fileSize = int(clientSocket.recv(1024).strip())
print('recv file size {}'.format(fileSize))
print('prepare to recv file...')

loop = fileSize // 1024
extend = fileSize % 1024
with open('to_recv_file/temp.jpg', 'wb') as f:
    for i in range(loop):
        recvfile = clientSocket.recv(1024)
        f.write(recvfile)
        clientSocket.send(b'1')
    recvfile = clientSocket.recv(extend)
    f.write(recvfile)
if os.path.getsize('to_recv_file/temp.jpg') == fileSize:
    clientSocket.send(b'0')
else:
    clientSocket.send(b'2')
print("recv end")
