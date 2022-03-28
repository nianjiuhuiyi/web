import socket


def client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        send_data = input("请输入要发送的数据：")
        print(send_data)
        if send_data == "exit":
            break
        client_socket.send(send_data.encode("utf-8"))

        # while True:  # 这里当客户端不需要接受消息
        #     receive_data = client_socket.recv(1024).decode("utf-8")
        #     # print("接收到的数据是：{}".format(receive_data))
        #     print("1111", receive_data)
        #     if not receive_data:
        #         break
        print("*******"*10, "\n"*3)

    client_socket.close()


if __name__ == '__main__':
    client("127.0.0.1", 8080)
