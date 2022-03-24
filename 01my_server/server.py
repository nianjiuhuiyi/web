import socket
import os
from pathlib import Path


def get_info(request_path):
    total_path = r"../static_source"
    result = None
    request_path = request_path[1:]
    if request_path:
        request_path += ".html"
    else:
        request_path = "index.html"
    path = Path(total_path).joinpath(request_path)

    if os.path.exists(path):
        result = path

    return result


def my_server():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("", 8080))
    tcp_server_socket.listen(128)

    # response的数据，最开始一定要有 `HTTP/1.1 200 OK` 这段文本，然后要显示的数据与这一行一定空一行
    # send_data = "HTTP/1.1 200 OK\r\n"   # 换行，为了兼容linux和windows
    # send_data += "\r\n"       # 上面也讲了一定要与显示的内容空一行（下面再拼接的显示内容）

    # # 这是把一个html页面发过了
    # with open(r"./show.html", encoding="utf-8") as fp:
    #     send_data += "".join(fp.readlines())

    while True:
        send_data = "HTTP/1.1 200 OK\r\n"  # 换行，为了兼容linux和windows
        send_data += "\r\n"  # 上面也讲了一定要与显示的内容空一行（下面再拼接的显示内容）

        a_client_socket, client_address = tcp_server_socket.accept()
        print("{}正在访问".format(client_address))
        # 接收一下浏览器的请求(目前不是必须的)
        request = a_client_socket.recv(1024).decode("utf-8")   # 注意decode解码
        print(request)

        route = request.split("\n")[0]
        route = route.split(" ")[1]

        route_path = get_info(route)
        if route_path is None:
            send_data += "<h1>此页面不存在 404 Not Found</h1>"
        else:
            with open(route_path, encoding="utf-8") as fp:
                print("\n", route, "\n")
                send_data += "".join(fp.readlines())

        a_client_socket.send(send_data.encode("utf-8"))


if __name__ == '__main__':
    my_server()
    # a = get_info(r"/c")
    # print(a)
