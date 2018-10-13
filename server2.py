import socket
import sys
import select


# Message Buffer size
MSG_BUFFER = 1024
# Obtaining the arguments using command line
try:
    HOST = sys.argv[1]
except:
    HOST = 'localhost'
try:
    PORT = int(sys.argv[2])
except:
    PORT = 8889

# Creating the client socket. AF_INET IP Family (v4)
# and STREAM SOCKET Type.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(4) # Listen ONLY ONE clients
print 'Client connected to %s:%s' % (HOST, PORT)
sockets = [serverSocket]

while True:
    ready_to_read, ready_to_write, _ = select.select(sockets, [], [])
    for sock in ready_to_read:
        if sock == serverSocket:
            sclient, addr = serverSocket.accept()  # Acepting client
            sockets.append(sclient)
            print "[SERVER] Client %s connected!" % str(sclient.getpeername())

        else:
            msg = sock.recv(MSG_BUFFER)
            if msg:
                print('<' + str(sock.getpeername()) + '>: ' + msg)
                if msg == ':smile':
                    print('[SERVER] :)')
            # disconnected
            else:
                print('<' + str(sock.getpeername()) + '>: disconnected :c')
                sockets.remove(sock)