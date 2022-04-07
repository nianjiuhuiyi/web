def set_func(a_func):
    print("这是加权限的装饰器")

    def call_func(*args, **kwargs):
        print("加的权限验证代码！")
        return a_func(*args, **kwargs)

    return call_func


def log_func(b_func):
    print("这是加日志的装饰器")

    def call_log_func(*args, **kwargs):
        print("这是记录日志的代码")
        return b_func(*args, **kwargs)

    return call_log_func


@set_func
@log_func
def my_func(num, *args, **kwargs):
    print("这是最开始的功能函数 %d" % num)


my_func(123)
