import os
import socket
import signal
import sys
from config import load_client_config

class Client_sockets:

    def __init__(self,sock_path,sock_type,sock_address,buffer_size):
        self.sock_path = sock_path
        if sock_type=='SOCK_STREAM':
            self.sock_type = socket.SOCK_STREAM
        if sock_address== 'AF_UNIX':
            self.sock_address = socket.AF_UNIX

        self.buffer_size = buffer_size
        self.running=True
    
        self.start()
    def find_msg_type(self):
        current_dir = os.getcwd()
        file_name = self.data
        file_path = os.path.join(current_dir, file_name)
        if(os.path.isfile(file_path)):
            with open(file_name, 'r') as f:
                self.data = f.read()
                return 'txt'
        elif type(self.data)==str:
            return 'string'
        elif type(self.data)==dict:
            return 'json'

    def shutdown(self, signum=None, frame=None):
        print("Shutdown signal received. Closing client...")
        self.running = False
        if hasattr(self, 'client_socket'):
            self.client_socket.close()
            sys.exit(0)
    def register_signal_handlers(self):
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)


    def send_data(self):
        try:
            #self.data=input("Enter a msg or File name ")
            self.msg_type=self.find_msg_type()

            self.client_socket.sendall(self.msg_type.encode('utf-8').ljust(10))
            self.client_socket.sendall(self.data.encode('utf-8'))
            return 1
        except BrokenPipeError as e:
            print("Connection has been ended by the server")
            return 0

    def get_resp(self):
        try:
            response = self.client_socket.recv(self.buffer_size)
        except Exception as e:
            print("Error in receiving data",e)
        return response.decode()

    def run(self):
        
        while(self.running):
            try:
                self.register_signal_handlers()
                self.data = input("enter data to be sent json or string or text file")
                
            except Exception as e:
                if self.running:
                    print(f"Error accepting client: {e}")
            fl = self.send_data()
            if fl==0:
                break
            if self.data=='q':
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
            self.register_signal_handlers()
        except Exception as e:
            print("Error happened in socket creation",e)
        finally:
            self.close()

    def close(self):
        try:
            self.client_socket.close()
        except Exception as e:
            print("socket has already closed",e)


#if __name__=="__main__":
    #sock_path = input("Enter your path where your server is listening")
  #  sock_path = "/tmp/my_socket"
 #   client = Client_sockets(sock_path)



