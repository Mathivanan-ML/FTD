import os
import socket
import signal,select
import sys
from config import load_client_config
from Logger import *

class Client_sockets:

    def __init__(self,sock_path,sock_type,sock_address,buffer_size,id):
        self.sock_path = sock_path
        if sock_type=='SOCK_STREAM':
            self.sock_type = socket.SOCK_STREAM
        if sock_address== 'AF_UNIX':
            self.sock_address = socket.AF_UNIX

        self.buffer_size = buffer_size
        self.running=True
        self.client_id =id
        self.max_req = 3
        self.cur_cnt = 0
        self.timeout = 3
        
        
        self.start()


    def start(self):
        try:
            self.cur_cnt+=1
            if self.cur_cnt>=self.max_req+1:
                self.close()
                exit(0)
            self.client_socket = socket.socket(self.sock_address,self.sock_type)
            self.connect()
            self.register_signal_handlers()
        except Exception as e:
            print("Error happened in socket creation",e)
        finally:
            self.close()

    def connect(self):
        try:
            self.client_socket.connect(self.sock_path)
            print(self.client_socket.getsockname())
            
            
            self.run()   
            
        except Exception as e:
            print("Error happened in client connection",e)

    def run(self):
        
        while(self.running):
            try:
                self.register_signal_handlers()
                print("Enter a msg or json or txt file: ")
                rlist, _, _ = select.select([sys.stdin], [], [], self.timeout) 
                if rlist: 
                    self.cur_cnt = 0
                    self.data = input()
                    
                else: 
                    print("Retrying...")
                    self.close()
                    self.start()
                    return
                # self.data = input("enter data to be sent json or string or text file")
                
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

    def get_resp(self):
        try:
            response = self.client_socket.recv(self.buffer_size)
        except Exception as e:
            print("Error in receiving data",e)
        return response.decode()

    def shutdown(self, signum=None, frame=None):
        print("Shutdown signal received. Closing client...")
        self.running = False
        if hasattr(self, 'client_socket'):
            self.client_socket.close()
            sys.exit(0)    

    def close(self):
        try:
            self.client_socket.close()
        except Exception as e:
            print("socket has already closed",e)





