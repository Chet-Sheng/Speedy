"""semaphore is a synchronization primitive that limits the number of concurrent tasks."""
import asyncio

# Define a semaphore with a limit
semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent tasks

async def limited_task(task_id, semaphore):
    async with semaphore:
        print(f"Task {task_id} is running")
        await asyncio.sleep(2)  # Simulating an I/O-bound task
        print(f"Task {task_id} is completed")

async def main():
    tasks = []
    for task_id in range(20):  # Suppose we have 20 tasks
        tasks.append(limited_task(task_id, semaphore))

    await asyncio.gather(*tasks)

asyncio.run(main())