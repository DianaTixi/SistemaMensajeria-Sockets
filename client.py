#Librerias
import socket   
import threading

username = input("Enter your username: ")

#LocalHost
host = '127.0.0.1'
#puerto disponible
port = 55555

#Creacion de un conector TCP/IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexion del cliente al servidor
client.connect((host, port))

#Funcion para recibir los mensajes desde el servidor
def recibir_mensaje():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Sucedio un error -- Desconectado")
            client.close
            break

#Funcion para enviar los mensajes al servidor y este lo entregue al cliente
def escribir_mensaje(): 
    while True:
        message = f"{username}: {input('')}" 
        client.send(message.encode('utf-8')) #El servidor envia a los demas clientes
# Creamos un hilo por funcion 
recibir_thread = threading.Thread(target=recibir_mensaje)
recibir_thread.start()

escribir_thread = threading.Thread(target=escribir_mensaje)
escribir_thread.start()