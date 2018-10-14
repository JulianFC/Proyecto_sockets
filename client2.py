import sys
import socket
import select
# comentario.
MSG_BUFFER = 1024

clientSocket = socket.socket()
try:
    host = sys.argv[1]
except:
    host = ''
try:
    port = sys.argv[2]
except:
    port = 8889

print "Write Username"
username = raw_input()

# Connecting
clientSocket.connect((host, port))
clientSocket.send(username)
print 'Connected to %s:%s' % (host, port)

SOCKET_LIST = []
SOCKET_LIST.append(sys.stdin) # standard input.
SOCKET_LIST.append(clientSocket)

print 'Welcome to the Best Chat in the World'

connected = True

while connected:
    ready_to_read, _, _ = select.select(SOCKET_LIST, [], [])
    message = raw_input("You: ")
    for sock in ready_to_read:
        if sock == clientSocket:
            msg = sock.recv(MSG_BUFFER)
            print(msg)

        clientSocket.send(message)
        if message == ":q":
            connected = False
            clientSocket.close()

