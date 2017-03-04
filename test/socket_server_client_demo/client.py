import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# clientSocket.setblocking(False)

server_address = ('127.0.0.1', 10000)




while True:
    clientSocket.connect(server_address)
    clientSocket.send(str.encode(":" + input()))
    recvInfo = clientSocket.recv(1024)
    print('recvInfo is : ', recvInfo.decode('utf-8'))
    clientSocket.shutdown(socket.SHUT_RDWR)
    clientSocket.close()
