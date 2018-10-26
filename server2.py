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
print 'Cliente conectado a %s:%s' % (HOST, PORT)

sockets = [serverSocket] #list of connected sockets
usernames = ["Server"] #list of connected usernames (in the same order as sockets)


#Have the server always on
while True:
    ready_to_read, ready_to_write, _ = select.select(sockets, sockets, [])
    for sock in ready_to_read: #for every sock sendig a message
        if sock == serverSocket:
            sclient, addr = serverSocket.accept()  # Acepting client
            sockets.append(sclient) #add to the list
            username = sclient.recv(MSG_BUFFER) #get username

            if username in usernames: #user already occupied
                sclient.send("wait") #send message to pick another message
                sockets.remove(sclient) #remove from list
            else:
                sclient.send("ok") #user available
                usernames.append(username) #add to list
                print "[SERVER]: Cliente <" + username + "> conectado."

        else:
            msg = sock.recv(MSG_BUFFER) #message received
            username = usernames[sockets.index(sock)]
            if msg:
                if msg == ":q": #disconnect user
                    print('[SERVER]: Cliente <' + username + '> se ha desconectado.')
                    usernames.remove(username)
                    sockets.remove(sock)
                elif msg == ":i": #print list of connected users
                        print('[SERVER]: Cliente <' + username + '> solicita Usuarios Conectados.')
                        for i in range(1, len(usernames)):
                            print('[' + str(i) + '] ' + usernames[i])

                elif msg == ":add": #send addres (the client prints it)
                    address = sock.getpeername()
                    sock.send("\nIdentificador Interno: " + address[0]+ " \nPuerto: "+ str(address[1]))

                elif msg[0:3] == ":p-": #send private message as ":p-username-message"
                    separators = []
                    for i in range(len(msg)):
                        if msg[i] == "-":
                            separators.append(i) #detect "-"
                    if len(separators) >= 2: #check correct format
                        target = msg[separators[0]+1:separators[1]] #user to send the message
                        if target in usernames: #check user available
                            message = msg[separators[1]+1:]
                            print('[SERVER]: Cliente <' + username + '> envia mensaja privado a <' + target + '>')
                            sockets[usernames.index(target)].send("[" + username + "]: " + message) #send message


                elif msg == ":h" or msg == ":q" or msg == ":i" or msg == ":add":
                    pass

                else:
                    print '[' + username + ']: ' + msg
            else:
                print('[SERVER]: Cliente <' + username + '> se ha desconectado.')
                usernames.remove(username)
                sockets.remove(sock)