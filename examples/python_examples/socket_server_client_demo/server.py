import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# serverSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)

serverSocket.bind(server_address)

serverSocket.listen(5)

(clientSocket, clientAddress) = serverSocket.accept()

print(clientAddress)

while True:
    recvInfo = clientSocket.recv(10).strip()
    # if len(recvInfo) == 0:
    #     print('0')
    # else:
    print(recvInfo)
    # print('recvInfo is : ', recvInfo.decode('utf-8'))
    # # clientSocket.send(recvInfo)
    # clientSocket.shutdown(socket.SHUT_RDWR)
    # clientSocket.close()
