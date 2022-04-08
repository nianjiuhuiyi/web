def set_level(level_num):
    print(789, level_num)

    def set_func(func):
        print(456)

        def call_func(*args, **kwargs):
            print(123)
            # 开始级别验证
            if level_num == 1:
                print("这是权限级别***1****")
            elif level_num == 2:
                print("这是权限级别***2****")
            else:
                print("没有权限")
            return func(*args, **kwargs)

        return call_func

    return set_func


# 这是装饰器里带了参数，
@set_level(2)
def my_func():
    print("这是写好的函数功能实现！")


# my_func()

"""
原理：(这种去做路由是最好的)
    - 在最开始的装饰 set_func 的基础上，又加了一层 set_level，这层负责加参数
    - 即便没有调用 my_func()， 导包都会自动运行 @set_level(2)， 
        - 就会立即执行 print(789, level_num) ，然后是 print(456)
    - 不会执行 print(123) ，要外部调用 my_func() 才行
"""
