class T:
    """
    这是一个描述信息,一般用三引号
    """

    def __str__(self):
        return "hello world!"

    pass


print(T.__doc__)  # 获取描述文档
print(help(T))  # 还可以这样获取描述

t = T()
print(t.__class__)  # 表示当前操作的对象的类是什么，结果 <class '__main__.T'>
print(t.__module__)  # 表示当前操作的对象在哪个模块，
# - 当前模块的类，结果就是  __main__
# - 当从其它模块导进来的类，输出就是其它模块的名字

"一个类中定义了 __str__ 方法，那么在print(t)时，默认输出该方法的返回值"
print(t)
# 还可以：
print("还可以这样用：%s" % t)

"""
__init__   初始化方法
__del__     一般无需定义，垃圾回收时会自动回收
__call__    实例对象()   加()时自动调用
__dict__    后去类或对象中的所有属性： t.__dict__  T.__dict__

"""

" __getitem__  __setitem__  __delitem__ "  # 用于索引操作，如字典，分别表示获取，设置，删除数据


class FOO:
    def __getitem__(self, key):
        print("__getitem__", key)

    def __setitem__(self, key, value):
        print("__setitem__", key, value)

    def __delitem__(self, key):
        print("__delitem__", key)


obj = FOO()  # obj并不是一个字典，但它里面实现了这三个魔法方法，就可以像字典这样操作
result = obj["k12"]
obj["k13"] = "world！"  # 它会这样把对应的值传到相应位置
del obj["k14"]

# 用于切片操作，如列表(这是Python2中的用法了，Python3中是把这整合到了上面的getitem三个中)
" __getslice__  __setslice  __delslice__  "


class A:
    def __getslice__(self, i, j):
        print("__getslice__", i, j)

    def __setslice__(self, i, j, sequence):
        print("__setslice__", i, j)

    def __delslice__(self, i, j):
        print("__delslice__", i, j)


a = A()
a[1: 3]  # 这里好像有些问题，总之就是让实例对象，可以实现像列表一样的操作
a[1: 3] = [11, 22, 33, 44, 55]
del a[3: 5]
