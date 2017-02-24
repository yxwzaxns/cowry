from socket import *
import ssl

# create an INET, STREAMing socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serverSocket.bind(('127.0.0.1', 2333))
# become a server socket
serverSocket.listen(5)

def deal_with_client(clientSocket):
    print("start Receiving file")

    # f = open('./tmp/d.jpg','wb')
    # info = clientSocket.recv(1024)
    # while info:
    print("Receiving...")
        # f.write(info)
    info = clientSocket.recv(1024)
    print(info.decode('utf8'))
    # start deal process
    sendInfo = str.encode(info.decode('utf8'))
    clientSocket.send(sendInfo)
    # f.close()
    print("complete")

while True:
    (clientSocket, clientAddress) = serverSocket.accept()
    print(clientSocket,'===', clientAddress)

    connstream = ssl.wrap_socket(clientSocket,
                                 server_side=True,
                                 certfile="./certs/server.crt",
                                 keyfile="./certs/server.key")
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(SHUT_RDWR)
        connstream.close()
