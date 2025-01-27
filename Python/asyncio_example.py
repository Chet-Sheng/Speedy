import asyncio

# asyncio.run() cannot be called when another asyncio event loop is running in the same thread, while ipython/colab is already running an event loop
# ref: https://stackoverflow.com/a/55409674


# ############################################################
async def process_batch(counter):
    """
    with async decorated, this is a coroutinue.
    process batch of messages through GNP and TMV

    Args:
        counter (_type_): 
    """
    print(f"batch_{counter}: OP_1")
    await asyncio.sleep(1)  # await means 

    print(f"batch_{counter}: OP_2")

async def main():
    # Run awaitable objects in the aws sequence concurrently.
    # If any awaitable in aws is a coroutine, it is automatically scheduled as a Task.
    # async_semaphore = asyncio.Semaphore(3)
    
    # below section is useless...
    # coroutines = []
    # for i in range(10):
    #     coroutines.append(process_batch(i))
    # async with async_semaphore:
    #     await asyncio.gather(*coroutines)
    task = []
    for i in range(10):
        task.append(process_batch(i))
        # breakpoint()
        # await asyncio.gather(*(process_batch(i) for i in range(10)))
        if len(task) >= 3:
            await asyncio.gather(*task)
            task = []
            print("=======")
        
    print("finished")

if __name__ == "__main__":
    asyncio.run(main())

# ############################################################
# ref: https://stackoverflow.com/questions/51045491/start-processing-async-tasks-while-adding-them-to-the-event-loop
import asyncio


NUM_ASYNCIO_TASKS = 3
NUM_TASKS = 8

async def some_task(i):
    print(f"task {i} starts running")
    await asyncio.sleep(3)
    if i == 1:
        print("sleeping 10s")
        await asyncio.sleep(20)
        print("finished sleeping!!!")  
        # slowest task won't block following task.
    print(f"task {i} finished!")

async def generate_tasks(loop):
    tasks = []
    for i in range(NUM_TASKS):  # mock kafka consumer
        counter = 0

        while len(tasks) >= NUM_ASYNCIO_TASKS:  # this is the predefined batch size
            if counter == 0:
                print("Maximum task capacity reached. Waiting...")
            tasks = [task for task in tasks if not task.done()]
            counter += 1
            await asyncio.sleep(1)

        # task is created and scheduled, will be executed when meeting next `await`
        task = loop.create_task(some_task(i))
        tasks.append(task)
        print(f"task {i} created by loop")
        await asyncio.sleep(0)  # ⬅️ 👀, force yielding to the event loop
    
    print("gather running now..")
    print(f"process remaining {len(tasks)} tasks")
    
    # This is important! it will wait for all unfinished tasks.
    # Without this line, the process will quite no matter if there are any all unfinished jobs
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(generate_tasks(loop))


######

import asyncio


NUM_ASYNCIO_TASKS = 3
NUM_TASKS = 8

async def some_task(i):
    print(f"task {i} starts running")
    await asyncio.sleep(3)
    if i == 1:
        print("sleeping 10s")
        await asyncio.sleep(20)
        print("finished sleeping!!!")  
        # slowest task won't block following task.
    print(f"task {i} finished!")

async def generate_tasks(loop):
    task = loop.create_task(some_task(1))

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(generate_tasks(loop))
