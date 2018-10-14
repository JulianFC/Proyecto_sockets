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
usernames = ["Server"]
while True:
    ready_to_read, ready_to_write, _ = select.select(sockets, [], [])
    for sock in ready_to_read:
        if sock == serverSocket:
            sclient, addr = serverSocket.accept()  # Acepting client
            sockets.append(sclient)
            username = sclient.recv(MSG_BUFFER)
            usernames.append(username)
            print "[SERVER] Client "+username+" connected!"

        else:
            msg = sock.recv(MSG_BUFFER)
            username = usernames[sockets.index(sock)]
            if msg:
                print '<' + username + '>: ' + msg
                if msg == ':smile':
                    print('[SERVER] :)')
                if msg == ":q":
                    usernames.remove(username)
                    sockets.remove(sock)


            # disconnected
            else:
                print('<' + username + '>: disconnected :c')
                usernames.remove(username)
                sockets.remove(sock)