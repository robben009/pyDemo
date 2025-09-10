import asyncio

# 定义协程
async def async_task(name, delay):
    print(f"任务 {name} 开始")
    await asyncio.sleep(delay)  # 模拟I/O操作（非阻塞）
    print(f"任务 {name} 完成（耗时{delay}秒）")
    return delay

# 方法1：直接运行单个协程
async def main():
    result = await async_task("A", 1)
    print(f"结果: {result}")

asyncio.run(main())  # Python 3.7+ 推荐用法

async def main():
    # 方式1： gather 批量运行（等待所有完成）
    results = await asyncio.gather(
        async_task("A", 1),
        async_task("B", 2),
        async_task("C", 1)
    )
    print(f"所有结果: {results}")  # [1, 2, 1]

    # 方式2：创建Task对象（可单独取消）
    task1 = asyncio.create_task(async_task("D", 3))
    task2 = asyncio.create_task(async_task("E", 1))
    await task1
    await task2

asyncio.run(main())


async def main():
    task = asyncio.create_task(async_task("A", 5))
    await asyncio.sleep(2)
    task.cancel()  # 取消任务
    try:
        await task
    except asyncio.CancelledError:
        print("任务已被取消")