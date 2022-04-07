def line(k, b):
    def cal(x):
        res = k * x + b
        return res
    return cal


line1 = line(2, 3)
print(line1(1))
print(line1(3))

line2 = line(5, 6)
print(line2(2))
print(line2(3))


# 这就是闭包，它有点类似于class，先使用line(k, b),返回cal函数的引用，
# 然后line1(x)的调用就是cal(x)的调用，它里面同时又用到了line函数中的变量 k、b,这就是闭包
# 如果要在cal 函数中修改 k或者b，那就是用关键字，nonlocal
