class Image:  # python3这里加不加(Object)都是一样的，Python2却有很大的区别
    def __init__(self, width, height):
        self.res = width * height

    @property  # 获取属性
    def size(self):
        return self.res  # 这个也一定要有返回值

    @size.setter
    def size(self, value):  # 因为设置属性，一定要传参数
        self.res = value

    @size.deleter
    def size(self):
        print("执行的这个函数")


# img = Image(460, 480)
# print(img.size)
# img.size = 45678
# print(img.size)
# del img.size

# ----------------------------------------------


class FOO:
    def get_bar(self):
        print("1.执行的这个get_bar")
        return "必须要有返回值"

    def set_bar(self, value):
        print("2.执行的这个set_bar")
        if isinstance(value, str):
            print("执行了赋值操作")
        else:
            print("输入有误，不是str，")

    def del_bar(self):
        print("3.deleter**********")

    # 这是类属性
    BAR = property(get_bar, set_bar, del_bar, "4.放一些string的说明文档")  # 四个参数不是必须传满


foo = FOO()
# 以下是调用
print(foo.BAR)  # 这就自动调用类属性BAR中第一个参数，即get_bar,,不能是foo.get_bar
foo.BAR = "new_strings"  # 自动调用第二个参数（在设置值时，可做一些检查）
del foo.BAR  # 自动调用第三个参数
print(FOO.BAR.__doc__)  # 获取第四个参数中设置的值，注意因为是类属性，用类FOO去调用
