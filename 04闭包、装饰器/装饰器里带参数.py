def add_args(key):
    print(789, key)
    def set_func(func):
        print(456)
        def call_func():
            print(123)
            func()
        return call_func
    return set_func


# 这是装饰器里带了参数，
@add_args("hello")
def my_func():
    print("原始的执行")

"""
原理：
    - 在最开始的装饰 set_func 的基础上，又加了一层 add_args，这层负责加参数
    - 即便没有调用 my_func()， 导包都会自动运行 @add_args("hello")， 
        - 就会立即执行 print(789, key) ，然后是 print(456)
    - 不会执行 print(123) ，要外部调用 my_func() 才行
"""


import flask