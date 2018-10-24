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
    PORT = 8880

# Creating the client socket. AF_INET IP Family (v4)
# and STREAM SOCKET Type.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(4) # Listen ONLY ONE clients
print 'Client connected to %s:%s' % (HOST, PORT)
sockets = [serverSocket]
usernames = ["Server"]

while True:
    ready_to_read, ready_to_write, _ = select.select(sockets, sockets, [])
    for sock in ready_to_write:
        print ready_to_write.index(sock)
    for sock in ready_to_read:
        if sock == serverSocket:
            sclient, addr = serverSocket.accept()  # Acepting client
            sockets.append(sclient)
            username = sclient.recv(MSG_BUFFER)

            if username in usernames:
                sclient.send("wait")
                sockets.remove(sclient)
            else:
                sclient.send("ok")
                usernames.append(username)
                print "[SERVER]: Client <" + username + "> Connected"

        else:
            msg = sock.recv(MSG_BUFFER)
            username = usernames[sockets.index(sock)]
            if msg:
                if msg == ":q":
                    print('[SERVER]: Client <' + username + '> Disconnected')
                    usernames.remove(username)
                    sockets.remove(sock)
                elif msg == ":i":
                        print('[SERVER]: Client <' + username + '> Solicita Usuarios Conectados.')
                        for i in range(1, len(usernames)):
                            print('[' + str(i) + '] ' + usernames[i])

                elif msg == ":add":
                    address, _ = sock.getpeername()
                    sock.send(address)

                elif msg[0:3] == ":p-":
                    msg = msg.split("-")
                    if msg[1] in usernames and len(msg) >= 3:
                        print('[SERVER]: Client <' + username + '> Sent Private Message to <' + msg[1] + '>')
                        sockets[usernames.index(msg[1])].send(msg[2])

                elif msg == ":h" or msg == ":q" or msg == ":i" or msg == ":add":
                    pass

                else:
                    print '[' + username + ']: ' + msg
                    if msg == ':smile':
                        print('[SERVER]: :)')
