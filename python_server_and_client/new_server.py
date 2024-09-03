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
                client_socket, _ = self.server_socket.accept()
                self.handle_Client()
            except Exception as e:
                print(f"Error accepting client: {e}")

    def handleClient(self):
        print("Client Connected")
        try:
            while True:
                self.data = self.client_socket.recv(1024)
                if not self.data:
                    print("Client disconnected")
                    break

                self.message = self.data.decode()
                if self.message == 'q':
                    print("Client sent 'q', disconnecting")
                    break

                print(f"Received: {self.message}")

                self.response = input("Enter a Msg: ")
                if(self.response=='q'):
                    exit(0)
                self.client_socket.sendall(self.response.encode('utf-8'))

        except BrokenPipeError:
            print("Connection terminated by the client")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.client_socket.close()



if __name__=='__main__':
    server=UnixSocket("/tmp/my_socket",1024,1)
    server.server_socket.close()
    os.remove(server.socket_file)

