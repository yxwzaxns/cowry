import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# serverSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)

serverSocket.bind(server_address)

serverSocket.listen(5)

(clientSocket, clientAddress) = serverSocket.accept()

print(clientAddress)
print('prepare to recv file...')

with open('to_recv_file/temp.jpg', 'wb') as f:
    recvfile = clientSocket.recv(1024)
    while recvfile:
        f.write(recvfile)
        recvfile = clientSocket.recv(1024)
print('recv end')
