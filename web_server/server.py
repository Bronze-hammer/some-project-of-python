
import socket
import sys

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
# 设置端口号
port = 9999

# setsockopt(level, optname, value)  设置给定套接字选项的值
#listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定端口
# bind() 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()

    print("连接地址: %s" % str(addr))

    msg='Think you for connecting'+ "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
