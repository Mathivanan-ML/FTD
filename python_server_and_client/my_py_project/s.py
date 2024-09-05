import socket
import uuid
import time
def get_unique_socket_id(sock):
    # Get the local address and port of the socket
    local_address = sock.getsockname()
    address_str = f"{local_address[0]}:{local_address[1]}"
    print(address_str)
    
    # Generate a unique identifier (UUID)
    unique_id = uuid.uuid4().hex
    
    # Combine the address and UUID to create a unique socket ID
    socket_id = f"{address_str}-{unique_id}"
    
    return socket_id

# Example usage
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))  # Bind to any available port
sock.listen(1)

unique_socket_id = get_unique_socket_id(sock)
print(f"Unique Socket ID: {unique_socket_id}")
time.sleep(10)
# Don't forget to close the socket when done
sock.close()
