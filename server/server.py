import socket
import ssl
import threading

sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

sslContext.load_cert_chain(certfile="./certs/server.crt", keyfile="./certs/server.key")
# create an INET, STREAMing socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to a public host, and a well-known port
serverSocket.bind(('127.0.0.1', 2333))
# become a server socket
serverSocket.listen(5)

def clientWorker(clientSocket, address):
    client = sslContext.wrap_socket(clientSocket,server_side=True)
    try:
        print("start Receiving file")

        # f = open('./tmp/d.jpg','wb')
        # info = clientSocket.recv(1024)
        # while info:
        print("Receiving...")
            # f.write(info)
        info = client.recv(1024)
        print(info.decode('utf8'))
        # start deal process
        sendInfo = str.encode(info.decode('utf8'))
        client.send(sendInfo)
        # f.close()
        print("complete")
    except Exception as e:
        print(e)
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

while True:
    (clientSocket, clientAddress) = serverSocket.accept()
    print(clientSocket,'===', clientAddress)
    threading.Thread(target = clientWorker,args = (clientSocket, clientAddress)).start()
