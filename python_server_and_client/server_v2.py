import os
import socket
class UnixSocket:
    def __init__(self,socket_file,size_of_msg,listeners):
        self.socket_file=socket_file
        self.size_of_msg=size_of_msg
        self.listeners=listeners

        self.setup()
    def setup(self):
        if os.path.exists(self.socket_file):
            os.remove(self.socket_file)
        self.server_socket=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        self.server_socket.bind(self.socket_file)

        self.server_socket.listen(self.listeners)

        print("Server is listening")

        self.server_available()
    def server_available(self):
        while True:
            try:
                self.client_socket, _ = self.server_socket.accept()
                self.handle_Client()
            except Exception as e:
                print(f"Error accepting client: {e}")

    def handle_Client(self):
        print("Client Connected")
        try:
            while True:
                msg_type = self.client_socket.recv(10).decode('utf-8').strip()
                if not msg_type:
                    print("Client disconnected")
                    break

                # Receive the data
                data = b''
                while True:
                    chunk = self.client_socket.recv(self.size_of_msg)
                    data += chunk
                    if len(chunk) < self.size_of_msg:
                        break
                if msg_type == 'txt':
                    self.save_file(data)
                elif msg_type == 'json':
                    self.process_json(data)
                else:
                    print(f"Received: {data.decode()}")
                    response = input("Enter a Msg: ")
                    if response == 'q':
                        exit(0)
                    self.client_socket.sendall(response.encode('utf-8'))
        except BrokenPipeError:
            print("Connection terminated by the client")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client_socket.close()

    def save_file(self, data):
        # Save the file received from the client
        with open('received_file', 'wb') as f:
            f.write(data)
        print("File saved as 'received_file'")

    def process_json(self, data):
        # Process JSON data
        try:
            json_data = json.loads(data.decode('utf-8'))
            print(f"Received JSON: {json_data}")
        except json.JSONDecodeError:
            print("Received invalid JSON")


if __name__=='__main__':
    server=UnixSocket("/tmp/my_socket",1024,1)
    server.server_socket.close()
    os.remove(server.socket_file)

