"""
Basic Async Patterns in Python

This file demonstrates fundamental asyncio patterns with practical examples.
Each pattern shows both correct and incorrect usage.

Jupyter/IPython runs its own event loop, so:
- `asyncio.get_running_loop()` returns Jupyter's loop
- `loop.run_until_complete()` fails because the loop is already running
- Direct `await` works because it uses the existing loop
"""

import asyncio
import time
import random
from typing import AsyncGenerator, List


# =============================================================================
# 1. BASIC COROUTINE PATTERNS
# =============================================================================

# UNDERSTANDING COROUTINES:
# - A coroutine is a function defined with 'async def'
# - When called, it returns a coroutine object (not the actual result)
# - To get the result, you must 'await' the coroutine
# - 'await' pauses the current coroutine until the awaited one completes

async def fetch_data(url: str, delay: float = 1.0) -> str:
    """
    Simulates fetching data from a URL with network delay.
    
    This is a COROUTINE FUNCTION because it's defined with 'async def'.
    When called, it doesn't execute immediately - it returns a coroutine object.
    """
    print(f"Fetching data from {url}...")
    
    # AWAIT EXPLAINED:
    # - 'await' pauses this coroutine until asyncio.sleep() completes
    # - During this pause, the event loop can run other coroutines
    # - This is what makes async code concurrent - we're not blocking!
    await asyncio.sleep(delay)  # Simulate network delay
    
    # RETURN IN ASYNC FUNCTIONS:
    # - Works the same as regular functions
    # - The returned value becomes the result when this coroutine is awaited
    return f"Data from {url}"


async def process_data(data: str) -> str:
    """
    Simulates processing data with computation delay.
    
    Another coroutine function that demonstrates chaining async operations.
    """
    print(f"Processing: {data}")
    
    # Another await - this coroutine will pause here
    # The event loop can run other tasks during this delay ⭐️
    await asyncio.sleep(0.5)  # Simulate processing time
    
    # Return the processed result
    return f"Processed: {data}"


async def basic_coroutine_example():
    """
    Example of basic coroutine usage with await.
    
    This demonstrates the fundamental pattern of async programming:
    1. Call async function with await
    2. Use the returned result
    3. Chain multiple async operations
    """
    
    # AWAIT PATTERN 1: Sequential execution
    # This line does several things:
    # 1. Calls fetch_data() which returns a coroutine object
    # 2. 'await' tells the event loop to run that coroutine ⭐️
    # 3. This function pauses until fetch_data() completes
    # 4. The result is assigned to 'data'
    print("Step 1: Starting data fetch...")
    data = await fetch_data("https://api.example.com")
    print(f"Step 1 complete: {data}")
    
    # AWAIT PATTERN 2: Using the result from previous await
    # We can use the result from the previous await as input to the next
    print("Step 2: Starting data processing...")
    result = await process_data(data)
    print(f"Step 2 complete: {result}")
    
    print(f"Final result: {result}")
    
    # RETURN IN ASYNC FUNCTION:
    # This return works like any function return
    # The caller who awaits this function will get this value
    return result


# DEMONSTRATION OF WHAT HAPPENS WITHOUT AWAIT:
async def demonstrate_without_await():
    """Shows what happens when you forget to use await."""
    
    print("\n--- Demonstrating the importance of await ---")
    
    # WITHOUT AWAIT - This is usually a mistake!
    # This gets a coroutine object, not the actual result
    coroutine_obj = fetch_data("https://example.com")
    print(f"Without await: {coroutine_obj}")
    print(f"Type: {type(coroutine_obj)}")
    
    # You need to clean up unused coroutines to avoid warnings
    coroutine_obj.close()
    
    # WITH AWAIT - This gets the actual result
    actual_result = await fetch_data("https://example.com")
    print(f"With await: {actual_result}")
    print(f"Type: {type(actual_result)}")


# NOTE: EXPLANATION OF THE EVENT LOOP'S ROLE: ⭐️
async def explain_event_loop():
    """
    Demonstrates how the event loop enables concurrency.
    
    The event loop is the heart of async programming:
    - It runs one coroutine at a time
    - When a coroutine hits 'await', it pauses and the loop runs another
    - This creates the illusion of multiple things happening at once
    """
    
    print("\n--- Event Loop Demonstration ---")
    print("This coroutine will pause multiple times...")
    
    print("Before first await")
    await asyncio.sleep(0.1)  # Pause here - event loop can run other code
    print("After first await")
    
    print("Before second await") 
    await asyncio.sleep(0.1)  # Pause here again
    print("After second await")
    
    print("Coroutine complete!")
    
    return "Event loop demo finished"


# =============================================================================
# 2. ASYNC GENERATOR PATTERNS
# =============================================================================

async def async_range(start: int, stop: int, delay: float = 0.1) -> AsyncGenerator[int, None]:
    """Async generator that yields numbers with delay."""
    current = start
    while current < stop:
        await asyncio.sleep(delay)  # Simulate async work
        yield current
        current += 1


async def async_generator_example():
    """Example of consuming an async generator."""
    print("Async generator example:")
    async for number in async_range(1, 6):
        print(f"Generated: {number}")


# =============================================================================
# 3. CONCURRENT EXECUTION PATTERNS
# =============================================================================

async def concurrent_tasks_example():
    """Example of running multiple tasks concurrently."""
    print("\n--- Concurrent Tasks Example ---")
    
    # Sequential execution (slower)
    start_time = time.time()
    await fetch_data("site1.com")
    await fetch_data("site2.com")
    await fetch_data("site3.com")
    sequential_time = time.time() - start_time
    print(f"Sequential execution took: {sequential_time:.2f} seconds")
    
    # Concurrent execution (faster)
    start_time = time.time()
    tasks = [
        fetch_data("site1.com"),
        fetch_data("site2.com"),
        fetch_data("site3.com")
    ]
    results = await asyncio.gather(*tasks)
    concurrent_time = time.time() - start_time
    print(f"Concurrent execution took: {concurrent_time:.2f} seconds")
    print(f"Results: {results}")
    
    return results


# =============================================================================
# 4. ERROR HANDLING PATTERNS
# =============================================================================

async def unreliable_task(task_id: int) -> str:
    """Simulates a task that might fail randomly."""
    await asyncio.sleep(random.uniform(0.1, 0.5))
    if random.random() < 0.3:  # 30% chance of failure
        raise Exception(f"Task {task_id} failed!")
    return f"Task {task_id} completed successfully"


async def error_handling_example():
    """Example of handling errors in async code."""
    print("\n--- Error Handling Example ---")
    
    tasks = []
    for i in range(5):
        tasks.append(unreliable_task(i))
    
    # Method 1: Using try/except with gather
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} succeeded: {result}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# =============================================================================
# 5. TIMEOUT PATTERNS
# =============================================================================

async def slow_operation(duration: float) -> str:
    """Simulates a slow operation."""
    await asyncio.sleep(duration)
    return f"Operation completed after {duration} seconds"


async def timeout_example():
    """Example of using timeouts with async operations."""
    print("\n--- Timeout Example ---")
    
    # Operation that should complete within timeout
    try:
        result = await asyncio.wait_for(slow_operation(1.0), timeout=2.0)
        print(f"Success: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")
    
    # Operation that will timeout
    try:
        result = await asyncio.wait_for(slow_operation(3.0), timeout=2.0)
        print(f"Success: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")


# =============================================================================
# 6. COMMON MISTAKES AND CORRECTIONS
# =============================================================================

# ❌ WRONG: Using await in non-async function
def wrong_sync_function():
    """This will cause a SyntaxError!"""
    # return await fetch_data("example.com")  # SyntaxError!
    pass


# ✅ CORRECT: Proper async function
async def correct_async_function():
    """This is the correct way to use await."""
    return await fetch_data("example.com")


# ❌ WRONG: Forgetting await (returns coroutine object, not result)
async def wrong_no_await():
    """This doesn't work as expected!"""
    result = fetch_data("example.com")  # This returns a coroutine, not the actual result!
    print(f"Result: {result}")  # Will print: <coroutine object fetch_data at 0x...>
    return result


# ✅ CORRECT: Using await to get the actual result
async def correct_with_await():
    """This works correctly."""
    result = await fetch_data("example.com")  # This gets the actual result
    print(f"Result: {result}")  # Will print: Result: Data from example.com
    return result


# ❌ WRONG: Using yield from in async function (SyntaxError in some contexts)
async def wrong_yield_from():
    """This might cause issues depending on the generator."""
    # yield from some_regular_generator()  # Can cause SyntaxError
    pass


# ✅ CORRECT: Using async for with async generators
async def correct_async_iteration():
    """This is the correct way to iterate over async generators."""
    async for item in async_range(1, 4):
        print(f"Item: {item}")


# =============================================================================
# 7. PRACTICAL EXAMPLE: WEB SCRAPER SIMULATION
# =============================================================================

async def fetch_url(url: str, session_id: int) -> dict:
    """Simulates fetching a URL with random delay and success rate."""
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    
    # Simulate different response scenarios
    if random.random() < 0.1:  # 10% chance of failure
        raise Exception(f"Failed to fetch {url}")
    
    return {
        "url": url,
        "status": 200,
        "content_length": random.randint(1000, 10000),
        "response_time": delay,
        "session_id": session_id
    }


async def web_scraper_example():
    """Practical example: concurrent web scraping simulation."""
    print("\n--- Web Scraper Example ---")
    
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
    ]
    
    # Create tasks for concurrent execution
    tasks = []
    for i, url in enumerate(urls):
        task = fetch_url(url, session_id=i)
        tasks.append(task)
    
    # Execute all tasks concurrently with error handling
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    successful = 0
    failed = 0
    total_time = 0
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Failed to fetch {urls[i]}: {result}")
            failed += 1
        else:
            print(f"✅ Successfully fetched {result['url']} "
                  f"({result['content_length']} bytes, "
                  f"{result['response_time']:.2f}s)")
            successful += 1
            total_time += result['response_time']
    
    print(f"\nSummary: {successful} successful, {failed} failed")
    if successful > 0:
        print(f"Average response time: {total_time/successful:.2f}s")


# =============================================================================
# 8. MAIN EXECUTION EXAMPLE
# =============================================================================

async def main():
    """Main function demonstrating all async patterns."""
    print("=== Basic Async Patterns Demo ===\n")
    
    # Run all examples
    await basic_coroutine_example()
    await demonstrate_without_await()
    await explain_event_loop()
    await async_generator_example()
    await concurrent_tasks_example()
    await error_handling_example()
    await timeout_example()
    await correct_async_iteration()
    await web_scraper_example()
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())