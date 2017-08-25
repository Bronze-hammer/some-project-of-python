import socket

# listen_socket = socket.socket()  创建socket对象
# listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket()

host = socket.gethostname()
port = 1234

# setsockopt(level, optname, value)  设置给定套接字选项的值
#listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind() 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
s.bind((host, port))

#等待客户端连接
s.listen(5)

while True:
    #建立客户端连接
    conn, addr = s.accept()
    print("Got connection from", addr)
    s.send("think you for connecting")
    s.close()
