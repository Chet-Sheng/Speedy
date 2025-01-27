import asyncio
import time

def long_running_task():
    print("Long running task started")
    time.sleep(5)  # blocking
    print("Long running task finished")

async def quick_async_task():
    print("Quick async task started")
    await asyncio.sleep(1)  # non-blocking
    print("Quick async task finished")

async def async_task():
    print("Async task started with long running task")
    await asyncio.to_thread(long_running_task)  # non-blocking: run sync operations in backend thread
    print("Async task continued with quick async task")
    await quick_async_task()  # non-blocking
    print("Async task finished")

async def main():
    # run 2 async ops and see their execution sequences:
    await asyncio.gather(
        async_task(),
        async_task(),
    )

asyncio.run(main())

# Async task started with long running task
# Long running task started
# Async task started with long running task
# Long running task started
# Long running task finished
# Long running task finished
# Async task continued with quick async task
# Quick async task started
# Async task continued with quick async task
# Quick async task started
# Quick async task finished
# Async task finished
# Quick async task finished
# Async task finished