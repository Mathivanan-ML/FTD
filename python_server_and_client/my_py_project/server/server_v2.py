import os
import socket
import json
import signal
import sys
from Logger import *
class UnixSocket:
    
    def __init__(self, socket_file, sock_type, sock_add, size_of_msg, listeners):
        self.socket_file = socket_file
        self.size_of_msg = int(size_of_msg)
        self.listeners = int(listeners)
        self.running = True  # To control the server loop

        self.sock_type = socket.SOCK_STREAM if sock_type == 'SOCK_STREAM' else None
        self.sock_add = socket.AF_UNIX if sock_add == 'AF_UNIX' else None
        self.idd=0
        if self.sock_type is None or self.sock_add is None:
            raise ValueError("Invalid socket type or address family")

        self.setup()

    def setup(self):
        if os.path.exists(self.socket_file):
            os.remove(self.socket_file)

        self.server_socket = socket.socket(self.sock_add, self.sock_type)
        self.server_socket.bind(self.socket_file)
        self.server_socket.listen(self.listeners)

        print("Server is listening...")
        self.register_signal_handlers()
        self.server_available()

    def register_signal_handlers(self):
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def server_available(self):
        while self.running:
            try:
                self.client_socket, _ = self.server_socket.accept()
                
                Logger(self.client_socket.fileno(),self.idd)
                self.idd=self.idd+1
                self.handle_client()
            except Exception as e:
                if self.running:
                    print(f"Error accepting client: {e}")

    def handle_client(self):
        print("Client Connected")

        try:
            while True:
                msg_type = self.client_socket.recv(10).decode('utf-8').strip()
                if not msg_type:
                    print("Client disconnected")
                    break

                data = self.receive_data()
                self.process_message(msg_type, data)
        except BrokenPipeError:
            print("Connection terminated by the client")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client_socket.close()

    def receive_data(self):
        data = b''
        while True:
            chunk = self.client_socket.recv(self.size_of_msg)
            data += chunk
            if len(chunk) < self.size_of_msg:
                break
        return data

    def process_message(self, msg_type, data):
        if msg_type == 'txt':
            self.save_file(data)
        elif msg_type == 'json':
            self.process_json(data)
        else:
            print(f"Received: {data.decode()}")
            response = input("Enter a Msg: ")
            if response == 'q':
                self.shutdown()
            self.client_socket.sendall(response.encode('utf-8'))

    def save_file(self, data):
        with open('received_file', 'wb') as f:
            f.write(data)
        print("File saved as 'received_file'")

    def process_json(self, data):
        try:
            json_data = json.loads(data.decode('utf-8'))
            print(f"Received JSON: {json_data}")
        except json.JSONDecodeError:
            print("Received invalid JSON")

    def shutdown(self, signum=None, frame=None):
        print("Shutdown signal received. Closing server...")
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    # Example usage
    server = UnixSocket('/tmp/my_socket', 'SOCK_STREAM', 'AF_UNIX', 1024, 5)
