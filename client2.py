import sys
import socket
import select
import sys

MSG_BUFFER = 1024

clientSocket = socket.socket()
try:
    host = sys.argv[1]
except:
    host = ''
try:
    port = sys.argv[2]
except:
    port = 8880

msg = "wait"

username = raw_input("Write Username: ")
clientSocket.connect((host, port))
clientSocket.send(username)
msg = clientSocket.recv(MSG_BUFFER)

while msg == "wait":
    # Connecting
    clientSocket.close()

    clientSocket = socket.socket()
    username = raw_input("Write new Username: ")
    clientSocket.connect((host, port))
    clientSocket.send(username)
    msg = clientSocket.recv(MSG_BUFFER)


print 'Connected to %s:%s' % (host, port)

SOCKET_LIST = []
SOCKET_LIST.append(sys.stdin) # standard input.
SOCKET_LIST.append(clientSocket)


print 'Welcome to the Best Chat in the World \n'

connected = True


while connected:

    print 'You: ',
    ready_to_read, _, _ = select.select(SOCKET_LIST, [], [])
    message = raw_input('\r')
    #message = sys.stdin.readline().strip()

    for sock in ready_to_read:
        clientSocket.send(message)

        if sock == clientSocket:
            msg = sock.recv(MSG_BUFFER)
            print(msg)

        if message == ":add":
            msg = clientSocket.recv(MSG_BUFFER)
            print '\nIdentificador Interno: ',
            print (msg + '\n')

        if message == ":h":
            print('\r \nComandos Disponibles:\n (:q) Salir del Chat. \n' +
                  ' (:i) Mostrar en Servidor a Todos los Usuarios.\n' +
                  ' (:add) Mostrar Identificador Interno. \n' +
                  ' (:p-name-msg) Envia Mensaje Privado "msg" a "name". \n')

        if message == ":q":
            connected = False
            print('\rYou Have Disconnected.')
            clientSocket.close()
