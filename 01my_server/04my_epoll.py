import socket
import re
import select


def deal_message(new_socket, receive_info):
    receive_info = receive_info.splitlines()
    print(receive_info[:3])
    print(">>>" * 20)
    ret = re.match("[^/]+(/[^ ]*)", receive_info[0])
    html_name = ""
    if ret:
        html_name = ret.group(1)
        if html_name == "/":
            html_name += "index.html"
    try:
        fp = open(r"./qt_static_source" + html_name, "rb")
    except:
        response_body = "这个页面找不到了！ 404 Not Found！".encode("utf-8")
    else:
        response_body = fp.read()
        fp.close()

    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
    response_head += "Content-Length: {}\r\n".format(len(response_body))
    response_head += "\r\n"

    new_socket.send(response_head.encode("utf-8"))  # 这个信息还需要编码
    new_socket.send(response_body)  # 这个是二进制读取的，就不用encode了


def my_server(port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 这一行一般不需要，这是设置当服务器先close，及服务器4次挥手之后资源能够立即释放，保证下次程序运行时可以立刻启动
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 设置为非堵塞的
    tcp_server_socket.setblocking(False)
    tcp_server_socket.bind(("", port))
    tcp_server_socket.listen(128)

    # (1)创建一个epoll对象（注意导包：import select）
    epl = select.epoll()
    select.epoll()
    # (2)将监听套接字对应的fd注册到epoll中
    # - 参数一：tcp_server_socket.fileno()获取套接字fd
    # - 参数二：select.EPOLLIN代表监听的事件是"recv的消息收取"（对应的应该还是消息发送哦）
    epl.register(tcp_server_socket.fileno(), select.EPOLLIN)

    fd_sockets = dict()
    while True:
        # (3)这会将其设置默认堵塞，直到os系统检测到数据到来， 通过事件通知方式告诉程序，此时才会解堵塞(fd_event_list中有一个或以上的套接字准备好收发数据了)
        # 返回的是一个list，因为可能有几个套接字都有数据，格式大概如下：
        # [(fd, event), ]  # fd:套接字对应的文件描述符，event：这个文件描述符到底是什么事件，例如调用recv接收等
        fd_event_list = epl.poll()
        # (4)上面第一次解堵塞，一定是tcp_server_socket这个套接字可以收数据了，此时fd_event_list里面应该就只有这一个套接字(上面.register的)
        for fd, event in fd_event_list:
            # 确定是server的那个套接字，才能去.accept()
            if fd == tcp_server_socket.fileno():
                a_client_socket, client_address = tcp_server_socket.accept()
                # 把产生的新的socket也register也进epoll，以监测它的情况
                epl.register(a_client_socket.fileno(), select.EPOLLIN)
                # 把client的socket何其对应的fd存起来（特比注意这里是a_client_socket.fileno()，不是fd）
                fd_sockets[a_client_socket.fileno()] = a_client_socket
            # 其实else也是等同于  elif event == select.EPOLLIN:  这可定是成立的
            else:  # 后面列表里逐渐加了client的socket
                # 这个时候我需要拿到client的socket对象去recv消息，但是现在拿到的是这个对对象的fd(所以上面要先存字典)
                receive_data = fd_sockets[fd].recv(1024).decode("utf-8")
                if receive_data:  # 注意可能收到的消息为空，代表断开连接
                    deal_message(fd_sockets[fd], receive_data)
                else:
                    fd_sockets[fd].close()
                    epl.unregister(fd)     # 客户端关闭后，也要把它从epl中拿出来
                    del fd_sockets[fd]  # 用完就移除字典


if __name__ == '__main__':
    my_server(8080)
    """
    浏览器访问查看示例： 127.0.0.1:8080     127.0.0.1:8080/    http://127.0.0.1:8080/classes.html
    注意：这个只能在linux下运行
    """
