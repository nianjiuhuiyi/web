import socket
import re
import threading
from dynamic_sources import dynamic


class MyServer:
    def __init__(self, port):
        self.port = port

    def run_forever(self):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server_socket.bind(("", self.port))
        tcp_server_socket.listen(128)

        while True:
            a_client_socket, client_address = tcp_server_socket.accept()
            print("{}正在访问".format(client_address))
            t = threading.Thread(target=self._deal_socket, args=(a_client_socket,))
            t.start()

    def _deal_socket(self, new_socket):
        receive_info = new_socket.recv(1024).decode("utf-8")
        print(">>>" * 20)
        # 下面使用正则将其解析出来
        receive_info = receive_info.splitlines()
        print(receive_info[:3])
        ret = re.match("[^/]+(/[^ ]*)", receive_info[0])
        file_name = ""
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name += "index.html"

        # 按照WSGI的约定，这个env需要传递字典，方便后续扩展
        env = dict()
        env["file_name"] = file_name
        # self._handle_header,传进来的参数，就决定header。用的变量是self.response_head
        response_body = dynamic.application(env, self._handle_header)

        new_socket.send(self.response_head.encode("utf-8"))
        new_socket.send(response_body.encode("utf-8"))
        new_socket.close()

    def _handle_header(self, header_status, header_args: (str, [(str, str), ])):
        """
        处理header的函数，通过传进来的函数把，self.response_head 处理成想要的
        """
        # response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"  # 为了拼接成这个样子
        self.response_head = "HTTP/1.1 "  # 每次都这样重置一下，不然就一直在累加了
        self.response_head += (header_status + "\r\n")
        for key, value in header_args:
            self.response_head += "{}: {}\r\n".format(key, value)
        # 最后加一个换行
        self.response_head += "\r\n"


def main():
    my_server = MyServer(8899)
    my_server.run_forever()


if __name__ == '__main__':
    main()
    """
    浏览器访问查看示例： 127.0.0.1:8899     127.0.0.1:8080/    http://127.0.0.1:8080/classes.html
    http://127.0.0.1:8080/licensing.html  等正确网页
    或这种不存在网页  http://127.0.0.1:8080/classes123456.html
    """
