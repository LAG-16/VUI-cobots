import socket
import json

host_ip = ''                 # Symbolic name meaning all available interfaces
port = 50007  # Arbitrary non-privileged port (50000, 9999)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_address = ((host_ip, port))
server_socket.bind(socket_address)
server_socket.listen(5)
key_save = []
print("Listen at: ", socket_address)
try:
    client_socket, address = server_socket.accept()
    with client_socket:
        print("Connection from: ", address)
        while True:
            with open("/home/tec/pytorch_yolov5/data.json", "r") as jsonFile:  # Local JSON in Jetson AGX
                color = json.load(jsonFile)
            jsonFile.close()
            for key, value in color.items():
                for string in value:
                    if string == 0:
                        key_save.append(key)
                    break
            for item in key_save:
                color.pop(item)
            color = str(color)
            key_save = []
            data = client_socket.recv(1024)
            if not data:
                client_socket.close()
                server_socket.close()
                break
            client_socket.send(color.encode())
except KeyboardInterrupt:
    client_socket.close()
    server_socket.close()
