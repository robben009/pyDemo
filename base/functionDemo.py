# 函数是第一类对象（First-Class Objects）。这意味着函数可以像其他数据类型一样被：
# 赋值给变量
# 作为参数传递给其他函数
# 作为函数的返回值
# 存储在数据结构中
# 函数可以赋值给变量
def say_hello():
    print("Hello!")

greeting = say_hello
greeting()  # 输出: Hello!

# 函数可以作为参数传递给其他函数
def execute(func):
    func()

execute(say_hello)  # 输出: Hello!

# 函数可以作为返回值
def get_greeting():
    return say_hello

greeting_func = get_greeting()
greeting_func()  # 输出: Hello!


# map()是一个高阶函数，接受一个函数和一个可迭代对象。
# 装饰器属于高阶函数（Higher-Order Function）的一种应用。高阶函数是指那些接受一个或多个函数作为参数，或者返回一个函数的函数
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)
print(list(squared))  # 输出: [1, 4, 9, 16, 25]


def outer_function(x):
    def inner_function(y):
        return x + y  # 内部函数可以访问外部函数的变量x
    return inner_function

closure = outer_function(10)
print(closure(5))  # 输出: 15



