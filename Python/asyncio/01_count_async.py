import asyncio

async def count():
    """each call to count is a single event loop, or coordinator"""
    print("One")
    # a coroutine is a function that can suspend its execution before reaching return, 
    # and it can indirectly pass control to another `coroutine` for some time.
    await asyncio.sleep(1)
    print("Two")

async def main():
    # Return a future aggregating results from the given coroutines/futures.
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# $ python3 count_async.py
# One
# One
# One
# Two
# Two
# Two
# count_async.py executed in 1.01 seconds.