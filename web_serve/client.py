
import socket

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 8888

listen_socket.connect((HOST, PORT))
print(listen_socket.recv(1024))
listen_socket.close()
