class MyFile:
    def __init__(self, file_name, mode):
        self.name = file_name
        self.mode = mode

    def __enter__(self):  # 没有参数
        print("entering")
        self.fp = open(self.name, self.mode)
        # 一些其它逻辑处理代码
        return self.fp  # 相当于把一开始的结果存起来了，方便后面调close时使用

    # 无论哪种情况，异常与否，系统都会调用这个方法
    def __exit__(self, *args):  # *args是我自己写的，并没用到
        print("will exit")
        self.fp.close()


# 这里的fp就是 __enter__ 方法的返回值
with MyFile("README.txt", "w") as fp:
    fp.write("hello world!")

# 这样就不用显示地调用close方法了，有系统自动去调用，哪怕中间遇到异常，close也会调用


# Python还提供了一个contextmanager的装饰器
from contextlib import contextmanager


@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()


# 调用：这样 my_open 函数也可以用with了
with my_open("README.txt", "r") as fp:
    data = fp.readlines()
    print(data)
