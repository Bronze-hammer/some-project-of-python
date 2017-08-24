import socket

# HOST 本地主机名；  PORT 端口
HOST = socket.gethostname()
PORT = 8888

# listen_socket = socket.socket()  创建socket对象
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# setsockopt(level, optname, value)  设置给定套接字选项的值
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind() 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
listen_socket.bind((HOST, PORT))
#等待客户端连接
listen_socket.listen(5)
print ('Serving HTTP on port %s ...' % PORT)
while True:
    #建立客户端连接
    listen_socket.address = listen_socket.accept()
    print("连接地址:", address)

    listen_socket.send("欢迎访问!")
    listen_socket.close()
