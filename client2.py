import sys
import socket
import select

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

# Connecting
clientSocket.connect((host, port))
print 'Connected to %s:%s' % (host, port)

SOCKET_LIST = []
SOCKET_LIST.append(sys.stdin) # standard input.
SOCKET_LIST.append(clientSocket)

print 'Welcome to the Best Chat in the World'
print 'You: '

while True:
    ready_to_read, _, _ = select.select(SOCKET_LIST, [], [])
    for sock in ready_to_read:
        if sock == clientSocket:
            msg = sock.recv(MSG_BUFFER)
            print(msg)
        message = raw_input("You: ")
        clientSocket.send(message)

