def set_func(a_func):
    def call_func():
        print("这是权限验证1****")
        a_func()
        print("可以在不修改源函数的情况下，在其前面或者后面执行加东西，但不能中间加")

    return call_func


@set_func  # 这行就等于下面原理里的：my_func = set_func(my_func)
def my_func():
    print("这是最开始的功能函数")


"""
这是装饰器的原理： 
    res = set_func(my_func)  # 把这个结果(一个函数对象)返回给 res
    res()    # 然后这个调用就会执行
    
    所以：
    # 因为python中同名会覆盖
    my_func = set_func(my_func)   # 括号里的 my_func还是上面单独定义的my_func
    # 赋值后，这时 my_func 就是指向了 set_func 的返回值(也是一个函数引用)，且它把前面单独定义的my_func覆盖了
    my_func()  # 这个结果就不会是执行单独定义的my_func函数的结果，（而这也就是装饰器的实现原理）

"""
