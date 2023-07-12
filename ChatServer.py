import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.clients.append(client_thread)
            print(f"New client connected: {client_address}")

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                try:
                    message = client_socket.recv(1024).decode("utf-8")
                    if not message:
                        break

                    self.log_message(message)
                    self.broadcast(message, client_socket)
                except ConnectionResetError:
                    break

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_thread in self.clients:
                client_socket = client_thread._args[0]
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(message.encode("utf-8"))
                    except BrokenPipeError:
                        self.clients.remove(client_thread)

    def log_message(self, message):
        with self.lock:
            with open("chat_log.txt", "a") as log_file:
                log_file.write(f"{message}\n")

if __name__ == "__main__":
    server = ChatServer("localhost", 5000)
    server.start()
