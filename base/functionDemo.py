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


# map()是一个高阶函数，接受一个函数和一个可迭代对象
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)
print(list(squared))  # 输出: [1, 4, 9, 16, 25]



