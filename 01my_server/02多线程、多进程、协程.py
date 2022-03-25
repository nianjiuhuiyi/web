import socket
import re
import multiprocessing
import threading
import gevent
from gevent import monkey
monkey.patch_all()      # 为了协程的使用


def deal_socket(new_socket):
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
    response_head += "\r\n"

    receive_info = new_socket.recv(1024).decode("utf-8")
    print(">>>" * 20)
    # 下面使用正则将其解析出来
    receive_info = receive_info.splitlines()
    print(receive_info[:3])
    ret = re.match("[^/]+(/[^ ]*)", receive_info[0])
    html_name = ""
    if ret:
        html_name = ret.group(1)
        if html_name == "/":
            html_name += "index.html"

    try:
        fp = open(r"./qt_static_source" + html_name, "rb")
    except Exception:
        response_body = "这个页面找不到了！ 404 Not Found！".encode("utf-8")
    else:
        response_body = fp.read()
        fp.close()

    new_socket.send(response_head.encode("utf-8"))
    new_socket.send(response_body)
    new_socket.close()


def my_server(port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind(("", port))
    tcp_server_socket.listen(128)

    while True:
        a_client_socket, client_address = tcp_server_socket.accept()
        print("{}正在访问".format(client_address))

        # # 开始使用多进程：
        # p = multiprocessing.Process(target=deal_socket, args=(a_client_socket, ))
        # p.start()
        # a_client_socket.close()   # 多进程要这句

        # 开始使用多线程：
        t = threading.Thread(target=deal_socket, args=(a_client_socket, ))
        t.start()
        # a_client_socket.close()  # 多线程一定不要这句

        # 开始使用协程：
        # gevent.spawn(deal_socket, a_client_socket)      # 这一句就够了，不要.join()什么的了


if __name__ == '__main__':
    my_server(8899)
    """
    浏览器访问查看示例： 127.0.0.1:8080     127.0.0.1:8080/    http://127.0.0.1:8080/classes.html
    http://127.0.0.1:8080/licensing.html  等正确网页
    或这种不存在网页  http://127.0.0.1:8080/classes123456.html
    """
