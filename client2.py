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

username = raw_input("Write Username: ")

# Connecting
clientSocket.connect((host, port))
clientSocket.send(username)
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

    for sock in ready_to_read:
        if sock == clientSocket:
            msg = sock.recv(MSG_BUFFER)
            print(msg)

        clientSocket.send(message)

        if message == ":h":
            print('\r \nComandos Disponibles:\n (:q) Salir del Chat. \n' +
                  ' (:i) Mostrar en Servidor a Todos los Usuarios.\n' +
                  ' (:add) Mostrar Identificador Interno. \n' +
                  ' (:p-name-msg) Envia Mensaje Privado "msg" a "name". \n')

        if message == ":q":
            connected = False
            print('\rYou Have Disconnected.')
            clientSocket.close()

