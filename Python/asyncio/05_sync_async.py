import asyncio
import time

# 定义一个耗时的同步函数
def long_running_task():
    print("Long running task started")
    time.sleep(5)  # 模拟耗时操作，比如复杂计算或同步IO等
    print("Long running task finished")

# 定义一个快速的异步任务
async def quick_async_task():
    print("Quick async task started")
    await asyncio.sleep(1)  # 异步等待，不会阻塞事件循环
    print("Quick async task finished")

# 定义一个异步函数，它调用了上面定义的同步和异步函数
async def async_task():
    print("Async task started with long running task")
    long_running_task()  # 这将阻塞事件循环
    print("Async task continued with quick async task")
    await quick_async_task()  # 这是非阻塞的
    print("Async task finished")

# 运行两个异步任务，观察它们的执行顺序和耗时
async def main():
    # 启动两个async_task来观察它们的行为
    await asyncio.gather(
        async_task(),
        async_task(),
    )

# 使用asyncio运行main函数
asyncio.run(main())

# Async task started with long running task
# Long running task started
# Long running task finished
# Async task continued with quick async task
# Quick async task started
# Async task started with long running task
# Long running task started
# Long running task finished
# Async task continued with quick async task
# Quick async task started  # 1st run quick task
# Quick async task finished
# Async task finished
# Quick async task finished  # 2nd run quick task
# Async task finished