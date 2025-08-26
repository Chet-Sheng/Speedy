Example Scripts from [Async IO in Python: A Complete Walkthrough – Real Python](https://realpython.com/async-io-python/#setting-up-your-environment)


## How asyncio Works: Cooperative Multitasking

asyncio uses a model called cooperative multitasking. This means that tasks (coroutines) explicitly tell the event loop when they can be paused so that other tasks can run. This is different from preemptive multitasking, where the operating system decides when to switch tasks, regardless of what they are doing.


### Here's the core idea:

- Event Loop: asyncio is built around an event loop. This is the central coordinator that manages and distributes the execution of different tasks.
Coroutines (async def): You define tasks as coroutines using async def. These are special functions that can be paused and resumed.
await Keyword: The magic happens with the await keyword. When a coroutine encounters await on an operation that might take time (e.g., I/O operations like reading a file, making a network request, or asyncio.sleep()), it does the following:
It signals to the event loop, "I'm going to wait for this operation to complete. In the meantime, you can run something else."
The event loop then suspends the current coroutine.
The event loop looks for other tasks that are ready to run and executes one of them.
Resuming: When the awaited operation completes (e.g., the file data is read, or the network response arrives), the event loop is notified. At some point, when it's that coroutine's turn again, the event loop will resume it from where it left off (right after the await statement).
Same Thread or Different Thread?

This is a crucial point: asyncio coroutines run concurrently, but typically within the same single thread.

Single-Threaded Concurrency: When the event loop pauses one coroutine (at an await point) and switches to another, it's all happening in the same thread. It's not creating new threads for each coroutine.
Not Parallelism: Because it's single-threaded, asyncio doesn't provide true parallelism in the sense of executing multiple pieces of code simultaneously on different CPU cores. For CPU-bound tasks where you want to leverage multiple cores, you'd typically use the multiprocessing module.
Why it's efficient for I/O-bound tasks: asyncio shines for I/O-bound operations. While one coroutine is waiting for a slow network response or disk read (which doesn't consume CPU), the event loop can switch to other coroutines to do useful work, rather than having the entire thread sit idle.
How Many Event Loops Are There Typically?

Typically, an asyncio application has one main event loop.

One Loop Per Thread: The standard and most common practice is to run a single event loop in the main thread of your application.
Managing Multiple Loops: While it's technically possible to run different event loops in different threads, this significantly increases complexity and is generally not recommended unless you have a very specific, advanced use case. Managing state and communication between different event loops can be challenging.
asyncio.get_event_loop() / asyncio.new_event_loop() / asyncio.set_event_loop(): asyncio provides functions to get the current event loop, create a new one, and set the event loop for the current context. However, for most applications, you'll interact with the default event loop implicitly or by getting it once and passing it around if needed.
In essence:

asyncio enables concurrency (many tasks making progress) on a single thread.
It relies on coroutines (async def) and the await keyword to cooperatively yield control to the event loop.
The event loop manages switching between these tasks when they are waiting for I/O or other await-able operations.
You usually work with one event loop per application or per thread if you're doing more complex setups.
If a coroutine performs a long-running, CPU-bound operation without using await, it will block the entire event loop, and no other coroutines in that loop will be able to run until it finishes. This is why asyncio is best suited for I/O-bound work or tasks that can be broken down into smaller, awaitable chunks.
You're asking some excellent questions that get to the heart of how asyncio enables concurrency in Python! Let's break it down:

1. How asyncio Works: The Event Loop and Cooperative Multitasking

Core Idea: asyncio is built around an event loop. Think of the event loop as a central coordinator. It manages and distributes execution time among different tasks (coroutines).

Coroutines (async def): These are special functions that can be paused and resumed. When you define a function with async def, calling it doesn't run it immediately. Instead, it returns a coroutine object.

The await Keyword: This is where the "pausing" happens. When a coroutine encounters an await expression (e.g., await asyncio.sleep(1) or await some_io_operation()), it tells the event loop: "I'm going to be waiting for this operation to complete. You can go and run something else in the meantime."
Yielding Control: At this await point, the coroutine yields control back to the event loop. The event loop can then look for other tasks that are ready to run and execute them.
Resuming: Once the awaited operation is complete (e.g., the sleep timer finishes, or the network data arrives), the event loop is notified. When it's that coroutine's turn again, the event loop resumes it from where it left off (right after the await).
Cooperative Multitasking: This model is called "cooperative multitasking" because the coroutines explicitly say when they can be paused (using await). They "cooperate" to share execution time. This is different from pre-emptive multitasking (used by threads), where the operating system can interrupt a task at almost any point.
Analogy:

Imagine a chef (the event loop) in a kitchen with several cooking tasks (coroutines):

Task A (Boil Water): The chef starts boiling water. This will take time. Instead of just standing there watching the pot (await boil_water()), the chef tells the kitchen manager (event loop), "I'm waiting for the water to boil," and moves on.
Task B (Chop Vegetables): The chef now picks up the task of chopping vegetables. This is an active task.
Water Boils: The pot whistles! The kitchen manager informs the chef.
Resume Task A: If the chef was in the middle of chopping or has finished, they can now go back to the boiling water (Task A resumes) and use it.
2. Same Thread or Different Thread?

Typically the Same Thread: asyncio achieves concurrency within a single thread. When a coroutine awaits, it's not that a new thread is spawned. The event loop, running in that one thread, simply switches its attention to another ready coroutine within that same thread.
No True Parallelism (for CPU-bound work in one process): Because it's usually single-threaded, asyncio doesn't provide true parallelism in the sense of using multiple CPU cores simultaneously for Python code execution within that single process. This is largely due to Python's Global Interpreter Lock (GIL), which allows only one thread to hold control of the Python interpreter at any given time.
Benefits for I/O-bound Tasks: asyncio shines for I/O-bound operations (e.g., network requests, file system operations, database calls). These tasks spend most of their time waiting for external operations to complete. While one coroutine is waiting for a network response, the event loop can switch to another coroutine to do other work, making efficient use of that waiting time.

Integrating with Threads/Processes for CPU-bound Work: If you have CPU-bound tasks (heavy computations) that you want to run in parallel to truly utilize multiple cores, you would typically combine asyncio with:
concurrent.futures.ThreadPoolExecutor: To run blocking I/O or CPU-bound tasks in separate threads, allowing the asyncio event loop to remain unblocked. You can await futures from these executors.
concurrent.futures.ProcessPoolExecutor: To run CPU-bound tasks in separate processes, bypassing the GIL for true parallelism.
3. How Many Event Loops Are There Typically?

Typically One Per Thread (or One Main Loop): In a standard asyncio application, you typically have one main event loop running in your main thread. asyncio.run(main_coroutine()) is the common way to start this loop and run your entry-point coroutine.
Inter-thread Communication: If you are working with multiple threads and need to interact with the asyncio event loop in one thread from another thread, asyncio provides thread-safe functions like loop.call_soon_threadsafe() and asyncio.run_coroutine_threadsafe().
Creating New Loops: While you can create new event loop instances (asyncio.new_event_loop()) and set them as the current loop for a specific thread (asyncio.set_event_loop()), it's less common for typical application structures. Most of the time, you're interacting with the single, default event loop for your asynchronous operations.
Context (e.g., IPython/Jupyter): As we discussed earlier, environments like IPython/Jupyter already manage an event loop. When you use asyncio there, it integrates with this existing loop, often with the help of libraries like nest_asyncio to allow asyncio to run "inside" the already running loop. So, from your code's perspective within a Jupyter cell, you're still working with the concept of an event loop, even if it's nested.
In summary:

asyncio uses an event loop and cooperative multitasking with async/await.
Coroutines pause at await and yield control, allowing other coroutines to run.
This happens within the same thread, making it great for I/O-bound concurrency but not for CPU-bound parallelism on its own.
Typically, an application has one main event loop, though you can manage loops per thread if needed for more complex scenarios.
This model provides a powerful way to write highly concurrent applications that can handle many operations (especially I/O-bound ones) efficiently without the overhead and complexities of traditional multi-threading in many cases.