
### socket模块

在网络编程中的一个基础组件就是套接字(socket)。套接字基本上是两个端点的程序之间的“信息通道”。

套接字包括两个：服务器套接字和客户机套接字。在创建一个服务器套接字后，让它等待连接。这样它就在某个网络地址处（IP地址和一个端口号的组合）监听，直到有客户端套接字连接。连接完成后，两者就可以进行交互。
处理客户端套接字通常比处理服务器端套接字容易，因为服务器必须准备随时处理客户端的连接，同时还要处理多个连接，而客户端只是简单的连接，完成事物，断开连接。

一个套接字就是socket模块中的socket类的一个实例。它的实例化需要三个参数：
* 第一个参数是地址族（默认是socket.AF_INET）；
* 第二个参数是流（socket.SOCK_STREAM，默认值）或者数据报（socket.SOCK_DGRAM）套接字；
* 第三个参数是使用的协议（默认是0，使用默认值即可）。

对于一个普通的套接字，不需要提供任何参数。

服务器端套接字使用bind方法后，再调用listen方法去监听某个特定的地址。客户端套接字使用connect方法连接到服务器，再connect方法中使用的地址与服务器在bind方法中的地址相同（在服务器端，能实现很多功能，比如使用函数socket.gethostname得到当前主机名）。在这种情况下，一个地址就是一个格式为（host,port）的元组，其中host是主机名（比如www.example.com），port是端口号（一个整数）。listen方法只有一个参数，即服务器未处理的连接长度（即允许排队等待的连接数目，这些连接在禁用之前等待）。

服务器端套接字开始监听后，它就可以接受客户端的连接。这个步骤使用accept方法来完成，这个方法会阻塞（等待）直到客户端连接，然后该方法就返回一个格式为（client,address）的元组，client是一个客户端套接字，address是一个前面解释过的地址。服务器在处理完与该客户端的连接后，再次调用accept方法开始等待下一次连接。这个过程通常都是在一个无限循环中实现的。

>这种形式的服务器端编程成为阻塞或者是同步网络编程

套接字有两个方法：send和recv（用于接收），用于传输数据。可以使用字符串参数调用send以发送数据，一个所需要的（最大）字节数做参数调用recv来接收数据。如果不能确定使用哪个数字比较好，那么1024是个很好的选择。

>使用的端口号一般是被限制的。在Linux或者Unix系统中，需要有系统管理员的权限才能使用1024以下的端口。这些低于1024的端口号被用于标准服务，比如端口80用于web服务（如果有的话）。如果用Ctrl+C停止了一个服务，可能要等上一段时间才能使用同一个端口号（否则可能会得到“地址正在使用”的错误信息）。