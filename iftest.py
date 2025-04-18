# # step1 让用户输入两个数值
# num1 = input("请输入第一个数值=")
# num2 = input("请输入第二个数值=")
# num1 = float(num1)
# num2 = float(num2)
#
# # step2 计算两个数值的和
# result = num1 + num2
#
# # step3 输出数值
# print(f"{num1}+{num2}的结果为：{result}")

# 99乘法表
# 问题化简：给定一个数值x，打印出从1~x之间的所有数字

for num in range(1, 10):
    nums = range(1, num + 1)
    for x in nums:
        print(f"{x} * {num} = {x * num}", end="\t")
    print("")  # 实现换行功能