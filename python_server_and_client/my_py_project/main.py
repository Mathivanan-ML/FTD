import sys
from client.client_v2 import Client_sockets
from server.server_v2 import UnixSocket
from config import load_client_config,load_server_config
def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <client|server>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == 'client':
        load_json = load_client_config()
        print(load_json.config)
        #sock_path = "/tmp/my_socket"
        Client_sockets(load_json.config["sock_path"], load_json.config['sock_type'],load_json.config['sock_address'],load_json.config['buffer_size'])

    elif mode == 'server':
        json_data = load_server_config()
        print(json_data.config)
        server = UnixSocket(json_data.config["socket_file"], json_data.config['sock_type'],json_data.config['sock_address'],json_data.config['size_of_msg'],json_data.config['listeners'])
        server.server_socket.close()
        os.remove(server.socket_file)
    else:
        print("Invalid mode. Use 'client' or 'server'.")
        sys.exit(1)

if __name__ == "__main__":
    main()

