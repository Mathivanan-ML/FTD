import os
import socket


class Client_sockets:

    def __init__(self,sock_path,sock_type=socket.SOCK_STREAM,sock_address=socket.AF_UNIX,buffer_size=1024):
        self.sock_path = sock_path
        self.sock_type = sock_type
        self.sock_address = sock_address
        self.buffer_size = buffer_size
        self.start()
    

    def send_data(self,data):
        try:
            self.client_socket.sendall(data.encode('utf-8'))
        except BrokenPipeError as e:
            print("Connection has been ended by the server")

    def get_resp(self):
        try:
            response = self.client_socket.recv(self.buffer_size)
        except Exception as e:
            print("Error in receiving data",e)
        return response.decode()

    def run(self):
        while(1):
            data = input("enter data to be sent")
            self.send_data(data)
            if data=='q':
                print("connection terminated by the client")
                break
            resp = self.get_resp()
            print("Received data from server: ",resp)

    def connect(self):
        try:
            self.client_socket.connect(self.sock_path)
            self.run()
        except Exception as e:
            print("Error happened in client connection",e)


    def start(self):
        try:
            self.client_socket = socket.socket(self.sock_address,self.sock_type)
            self.connect()
        except Exception as e:
            print("Error happened in socket creation",e)
        finally:
            self.close()

    def close(self):
        try:
            self.client_socket.close()
        except Exception as e:
            print("socket has already closed",e)


if __name__=="__main__":
    #sock_path = input("Enter your path where your server is listening")
    sock_path = "/tmp/my_socket"
    client = Client_sockets(sock_path)



