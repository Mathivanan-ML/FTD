import os
import socket
socket_file='/tmp/my_socket'
if os.path.exists(socket_file):
    os.remove(socket_file)

server_socket=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

server_socket.bind(socket_file)

server_socket.listen(1)

print("Server is listening")
while(1):
    try:
        client_socket,client_address=server_socket.accept()

        print("Client Connected")
        try:
            while(True):
                data=client_socket.recv(1024)
                if data.decode()=='q':
                    print("client disconnected")
                    client_socket.close()
                    break
                print("Received: ",data.decode())
                a=input("Enter a Msg")
                if(a=='q'):
                    exit(0)
        
                client_socket.sendall(a.encode('utf-8'))

        except BrokenPipeError:
            print("Connection terminated by the client")
        except Exception as e:
            print("Client is Not Active",e)
         
    except Exception as e:
        print("problem in accepting clients",e)

    
server_socket.close()
os.remove(socket_file)
