class MyDec(object):
    def __init__(self, func):
        self.func = func  # 传进来的是一个函数引用

    def __call__(self, *args, **kwargs):
        print("这是类做装饰器打印出来的")
        return self.func(*args, **kwargs)


# 既然MyDec是类名，那也是可以用调用静态方法的，如 @MyDec.静态方法
@MyDec  # 它的原理其实也是 get_str = MyDec(get_str)
def get_str():
    return "hello world!"


print(get_str())  # 所以此时的 get_str 是一个实例对象，用()就会调用__call__魔法方法
