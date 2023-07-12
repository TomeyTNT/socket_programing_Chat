import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except ConnectionResetError:
            break

def send_message(client_socket):
    while True:
        message = input("Input Massage: ")
        client_socket.sendall(message.encode("utf-8"))

# Connect to the server
server_host = "localhost"
server_port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Start receiving and sending messages in separate threads
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_thread = threading.Thread(target=send_message, args=(client_socket,))
send_thread.start()
