print('装饰器')
class C():
    get_password_callback = None
    def get_password(self, f):
        print('1')
        self.get_password_callback = f
        return f

    def prints(self):
        if self.get_password_callback:
            self.get_password_callback()
        else:
            print(0)

c = C()
c.prints() # 输出 0
@c.get_password # 输出 1
def b():
    print(2)
c.prints() # 输出 2
# 输出
# 0 
# 1
# 2

print('装饰器调用顺序')
def a(f):
    print(1)
    return f
def b(f):
    print(2)
    return f
def c(f):
    print(3)
    return f
@a
@b
@c
def d():
    print(4)

# 实际调用运行顺序为
# d = a(b(c(d)))

# 没有调用d()时
# 输出为 3 2 1

# 调用d()
d()
# 输出为 4

# Python装饰器的代码执行顺序(https://www.jianshu.com/p/a58d6f71b1ce)