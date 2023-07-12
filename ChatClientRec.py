import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print("Received message:", message)
        except ConnectionResetError:
            break

# Connect to the server
server_host = "localhost"
server_port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()
