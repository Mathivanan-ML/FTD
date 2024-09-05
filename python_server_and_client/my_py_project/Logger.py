from datetime import datetime
import uuid

class Logger:

    def __init__(self,fd):
        self.time = datetime.now()
        self.uid = self.get_unique_socket_id(fd)
        self.socket_str = self.store_in_logs()

    def get_unique_socket_id(sock):
    
        # local_address = sock.getsockname()
        # address_str = f"{local_address[0]}:{local_address[1]}"
        
      
        unique_id = uuid.uuid4().hex
        
      
        socket_id = f"{self.time}-{unique_id}"
        
        return socket_id

    def store_in_logs(self):

        with open('logs.txt', 'a') as file:
    
            file.write(self.socket_str)