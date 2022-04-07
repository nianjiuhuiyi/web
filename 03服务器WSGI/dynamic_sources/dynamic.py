import time

now_time = time.ctime()


def register():
    return "hello world!  {}".format(now_time)


def logging():
    return "这是一个登录页面！ {}".format(now_time)


def exiting():
    return "这是注销页面！ {}".format(now_time)


def application(env: dict, start_response):
    start_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])

    file_name = env["file_name"]
    if file_name.endswith(".py"):
        if file_name.endswith("register.py"):
            return register()
        elif file_name.endswith("logging.py"):
            return logging()
        elif file_name.endswith("exiting.py"):
            return exiting()
        else:
            return "这个页面找不到了！ 404 Not Found！"
    else:
        try:
            # 一定注意，这里./static_sources这个相对路径是相对的server.py(因为是从server.py启动的)，而不是dynamic.py
            fp = open(r"./static_sources" + file_name, "r")
        except Exception:
            response_body = "这个页面找不到了！ 404 Not Found！"
        else:
            response_body = fp.read()
            fp.close()
        return response_body
