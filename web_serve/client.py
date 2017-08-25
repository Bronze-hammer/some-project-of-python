
import socket

#listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket()

host = socket.gethostname()
port = 1234

s.connect((host, port))

print(s.recv(1024))
