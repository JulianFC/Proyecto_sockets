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
    port = 8889

username = raw_input("Escribe nombre de usuario: ") #ask for username
clientSocket.connect((host, port)) #connect
clientSocket.send(username)
msg = clientSocket.recv(MSG_BUFFER)

while msg == "wait": #if username is not available

    clientSocket.close() #discconect

    clientSocket = socket.socket() #create new socket
    username = raw_input("Nombra de usuario ocupado, escribe otro ") #ask another username
    clientSocket.connect((host, port))
    clientSocket.send(username)
    msg = clientSocket.recv(MSG_BUFFER)
    #repeat until username is available


print 'Conectado a %s:%s' % (host, port)

SOCKET_LIST = []
SOCKET_LIST.append(sys.stdin) # standard input.
SOCKET_LIST.append(clientSocket)


print 'Bienvenido a nuestro chat \n'

connected = True


while connected:

    print 'Tu: ',
    ready_to_read, _, _ = select.select(SOCKET_LIST, [], [])
    message = raw_input('\r') #read message to send

    for sock in ready_to_read:
        clientSocket.send(message) #send message

        if sock == clientSocket:
            msg = sock.recv(MSG_BUFFER)
            print(msg)

        if message == ":add": #if ask for address
            msg = clientSocket.recv(MSG_BUFFER) #read message
            print (msg + '\n')

        if message == ":h": #show available commands
            print('\r \nComandos Disponibles:\n (:q) Salir del Chat. \n' +
                  ' (:i) Mostrar en Servidor a Todos los Usuarios.\n' +
                  ' (:add) Mostrar Identificador Interno. \n' +
                  ' (:p-name-msg) Envia Mensaje Privado "msg" a "name". \n')

        if message == ":q": #disconnect
            connected = False
            print('\rTe has desconectado.')
            clientSocket.close()
