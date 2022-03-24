import socket
import re


def deal_socket(new_socket):
    # (1)response的数据，最开始一定要有 `HTTP/1.1 200 OK` 这段文本，然后要显示的数据与这一行一定空一行
    # (2)后面这个Content-Type: text/html;charset=utf-8算是固定的，告诉浏览器用utf-8解码，不然用gbk就会出现乱码
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"  # 换行，为了兼容linux和windows
    response_head += "\r\n"  # (3)上面也讲了一定要与显示的内容空一行（下面再拼接的显示内容）

    receive_info = new_socket.recv(1024).decode("utf-8")  # (4)注意decode解码
    print(receive_info)  # (5)收到的请求信息，是一整个字符串，第一行一定是类似于  GET / HTTP/1.1
    print(">>>" * 20)
    # 下面使用正则将其解析出来
    receive_info = receive_info.splitlines()  # (6)注意直接按行切割了
    ret = re.match("[^/]+(/[^ ]*)", receive_info[0])  # (7)注意这个正则的写法
    html_name = ""
    if ret:
        html_name = ret.group(1)  # 这就是上面正则小括号括()起来的号
        if html_name == "/":  # 针对只输入了 127.0.0.1:8080 后面没跟具体地址
            html_name += "index.html"  # 那就让其进入到导航首页

    try:
        fp = open(r"./qt_static_source" + html_name, "rb")  # (8)直接二进制打开，免得后面再编码
    except Exception:  # 出错一般就是没有这个页面，那就404
        response_body = "这个页面找不到了！ 404 Not Found！".encode("utf-8")
    else:  # (9)当try没有异常时会执行 else 块
        response_body = fp.read()  # 直接read()全部读取
        fp.close()
    # (10)可以分开发送的，并不是要一次性发完
    new_socket.send(response_head.encode("utf-8"))  # 这个信息还需要编码
    new_socket.send(response_body)  # 这个是二进制读取的，就不用encode了
    new_socket.close()  # (11)记得关闭socket


def my_server():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 这一行一般不需要，这是设置当服务器先close，及服务器4次挥手之后资源能够立即释放，保证下次程序运行时可以立刻启动
    # tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind(("", 8080))
    tcp_server_socket.listen(128)

    while True:
        a_client_socket, client_address = tcp_server_socket.accept()
        print("{}正在访问".format(client_address))
        # 把这个新产生的socket传到函数中去处理
        deal_socket(a_client_socket)


if __name__ == '__main__':
    my_server()
    """
    浏览器访问查看示例： 127.0.0.1:8080     127.0.0.1:8080/    http://127.0.0.1:8080/classes.html
    http://127.0.0.1:8080/licensing.html  等正确网页
    或这种不存在网页  http://127.0.0.1:8080/classes123456.html
    """
