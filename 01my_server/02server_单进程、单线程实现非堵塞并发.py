import socket

"""
阻塞/同步：打一个电话一直到有人接为止
非阻塞：打一个电话没人接，每隔10分钟再打一次，知道有人接为止
异步：打一个电话没人接，转到语音邮箱留言（注册），然后等待对方回电（call back)
看起来异步是最高效，充分利用资源，可以想像整个系统能支持大规模并发。但问题是调试很麻烦，不知道什么时候call back。
"""


def no_block_server(port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("", port))
    tcp_server_socket.listen(128)

    # 将套接字设为非堵塞
    tcp_server_socket.setblocking(False)

    # 用于保存连接上的客户端创建的新的socket
    wait_sockets = list()
    while True:  # 这个循环是保证有新的客户端可以链接进来
        try:  # 非堵塞的话，一定要try起来，不然没客户端连接，是没有返回值的，立马报错
            new_socket, new_socket_address = tcp_server_socket.accept()
        except:
            pass
        else:  # 有客户端连接了，就把它添加进列表
            new_socket.setblocking(False)  # 建议也设置上，因为上面的.setblocking(False)，测试不要这行，new_socket也成为了非堵塞，就有些疑惑
            wait_sockets.append((new_socket, new_socket_address))

        # 循环所有的链接上了的socket
        for a_wait_socket in wait_sockets:
            try:
                # 0是socket，1是其对应的地址
                receive_data = a_wait_socket[0].recv(1024).decode("utf-8")
            except:
                # 没有数据发过来时，因为非阻塞，就会报错，就会进到这个里面
                pass
            else:
                # 当没有发生异常，说明new_socket收到来自客户端的消息了,分两种情况：
                # - 字符串不为空，这就是收到的消息
                # - 如果字符串为空，就说明客户端的socket已经调用了 .close() 了，就可以退出了，服务器端的这个也可以调用.close()了
                if receive_data:
                    print("正在访问的是：{}".format(a_wait_socket[1]), receive_data)
                else:
                    # 代表收到空字符了，说明客户端断开连接了
                    a_wait_socket[0].close()   # 关闭连接
                    wait_sockets.remove(a_wait_socket)  # 从等待列表移出去


if __name__ == '__main__':
    no_block_server(8080)
