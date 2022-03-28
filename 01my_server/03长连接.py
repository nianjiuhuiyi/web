import socket
import re


def deal_message(new_socket, receive_info):
    # 下面使用正则将其解析出来
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
        fp = open(r"./qt_static_source" + html_name, "rb")  # (8)直接二进制打开，免得后面再编码
    except:
        response_body = "这个页面找不到了！ 404 Not Found！".encode("utf-8")
    else:
        response_body = fp.read()  # 直接read()全部读取
        fp.close()

    # (1)response的数据，最开始一定要有 `HTTP/1.1 200 OK` 这段文本，然后要显示的数据与这一行一定空一行
    # (2)后面这个Content-Type: text/html;charset=utf-8算是固定的，告诉浏览器用utf-8解码，不然用gbk就会出现乱码
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
    # (3)(重点：)这一行就是告诉浏览器我们发的数据有多长，加之没有.close()的调用，不然就会一直在转圈加载
    response_head += "Content-Length: {}\r\n".format(len(response_body))  # 可以直接len()数据body的二进制形式
    response_head += "\r\n"  # 换行，为了兼容linux和windows

    # (10)可以分开发送的，并不是要一次性发完
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

    wait_sockets = list()
    while True:
        try:
            a_client_socket, client_address = tcp_server_socket.accept()
        except:
            pass
        else:
            a_client_socket.setblocking(False)
            wait_sockets.append((a_client_socket, client_address))

        for a_wait_socket in wait_sockets:
            try:
                receive_data = a_wait_socket[0].recv(1024).decode("utf-8")
            except:
                pass
            else:
                if receive_data:
                    # 这里就会发现有相同套接字的请求，验证了长连接
                    print("收到了{}的请求！".format(a_wait_socket[1]))
                    deal_message(a_wait_socket[0], receive_data)
                else:
                    a_wait_socket[0].close()
                    wait_sockets.remove(a_wait_socket)


if __name__ == '__main__':
    my_server(8080)
    """
    浏览器访问查看示例： 127.0.0.1:8080     127.0.0.1:8080/    http://127.0.0.1:8080/classes.html
    http://127.0.0.1:8080/licensing.html  等正确网页
    或这种不存在网页  http://127.0.0.1:8080/classes123456.html
    """
