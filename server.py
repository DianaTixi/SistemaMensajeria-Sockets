#Librerias
import socket   
import threading

#IP LocalHost
host = '127.0.0.1'
#Puerto Disponible
port = 55555

#Creacion de un conector TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Asociamos el conector con el host y el puerto
server.bind((host, port))
#Ponemos al conector en modo servidor
server.listen()
# Verificacion de que el servidor esta corriendo
print(f"Servidor de Chat {host}:{port}")
#Lista para guardar los clientes
clients = []
#Lista para los nombres de los clientes
usernames = []

#Funcion para enviar el mensaje a todos los clientes
def envioMensaje(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

#Funcion para el manejo de mensajes
def mensaje(client):
    while True:
        try:
            message = client.recv(1024) #Leemos los datos de la conexion
            envioMensaje(message, client)
        except:
            index = clients.index(client) #Para obtener el usermane del cliente
            username = usernames[index] # Obtenemos el username
            envioMensaje(f"Chat: {username} disconnected".encode('utf-8'), client) #codificamos el string en 
            clients.remove(client)
            usernames.remove(username)
            client.close() #Cerramos la conexion del cliente
            break

#Funcion para el manejo de conexiones retorna dos valores (IP y Puerto)
def conexion():

    while True:
        #Esperamos que se accepte la conexion
        client, address = server.accept()
        client.send("@username".encode("utf-8")) 
        username = client.recv(1024).decode('utf-8') #Leemos los datos de la conexion
        clients.append(client) # Agregamos a la lista de clientes
        usernames.append(username) #Agregamos a la lista de username
        print(f"{username} esta conectado con la IP {str(address)}")
        message = f"Chat: {username} se conecto a sistema de mensajeria!".encode("utf-8")
        envioMensaje(message, client)
        client.send("Conectado al Servidor".encode("utf-8"))
        #Creamos un hilo por cliente, para el manejo de los mensajes de forma independiente
        thread = threading.Thread(target=mensaje, args=(client,))
        thread.start()

conexion()