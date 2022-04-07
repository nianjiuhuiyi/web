def set_func(a_func):
    def call_func(*args, **kwargs):   # 这里就固定写法吧，这样多少个参数都能处理
        print("加的权限验证代码！")
        # 万一被装饰的函数有返回值，就这里加个return就好了，是通用的
        return a_func(*args, **kwargs)      # 下面这样原封不动的传进去
    return call_func


@set_func  # 这行就等于下面原理里的：my_func = set_func(my_func)
def my_func(num, *args, **kwargs):
    print("这是最开始的功能函数 %d" % num)
    print("有多的参数嘛：", args)
    print("多个字典参数：", kwargs)


my_func(100)
my_func(100, 20)
my_func(100, 20, age=25)

