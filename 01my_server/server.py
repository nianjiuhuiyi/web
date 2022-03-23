import socket


def my_server():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("", 8080))
    tcp_server_socket.listen(128)

    # response的数据，最开始一定要有 `HTTP/1.1 200 OK` 这段文本，然后要显示的数据与这一行一定空一行
    send_data = "HTTP/1.1 200 OK\r\n"   # 换行，为了兼容linux和windows
    send_data += "\r\n"       # 上面也讲了一定要与显示的内容空一行（下面再拼接的显示内容）

    # 这是把一个html页面发过了
    with open(r"./show.html", encoding="utf-8") as fp:
        send_data += "".join(fp.readlines())

    while True:
        a_client_socket, client_address = tcp_server_socket.accept()
        print("{}正在访问".format(client_address))
        # 接收一下浏览器的请求(目前不是必须的)
        request = a_client_socket.recv(1024).decode("utf-8")   # 注意decode解码
        print(request)
        a_client_socket.send(send_data.encode("utf-8"))


if __name__ == '__main__':
    my_server()
