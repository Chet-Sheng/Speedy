#!/usr/bin/env python3
# rand.py

import asyncio
import random

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def make_random(idx: int, threshold: int = 6) -> int:
    """A corountine keeps producing random integers in the range[0, 10] til hitting threshold.
    Most programs will contain small, modular coroutines and one wrapper function
    that serves to chain each of the smaller coroutines together.

    Parameters
    ----------
    idx : int
        color index for better visualisation purpose
    threshold : int, optional
        stop threshold, by default 6

    Returns
    -------
    int
        The final generated integer bigger than threshold
    """
    # c[idx + 1] is just about coloring the printed out string
    print(c[idx + 1] + f"Initiated make_random({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"make_random({idx}) == {i} too low; retrying.")
        # NOTE: let multiple calls of this coroutine not need to wait for each other to complete in succession.
        # Mimic IO-bound process where there is uncertain wait time involved.
        await asyncio.sleep(idx + 1)

        i = random.randint(0, 10)

    print(c[idx + 1] + f"---> Finished: make_random({idx}) == {i}" + c[0])
    return i

async def main():
    # Return a future aggregating results from the given coroutines/futures.
    # Chet: coroutine is an extension of generator, that's why using generator expression here?
    # Chet: tried making `()` => `[]`, everything is same
    res = await asyncio.gather(*(make_random(i, 10 - i - 1) for i in range(3)))
    return res

if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())  # coming from `return` 
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")
