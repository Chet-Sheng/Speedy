from pathlib import Path
import random
import time

from locust import User, tag, task, constant, events


class ToyStressTest(User):
    wait_time = constant(0)
    idx=0

    @tag("tag1")
    @task
    def similarity_search(self):
        start_time = time.time()
        
        try:
            if self.idx > 3_000_000:
                10/0
            
            res = 1+1
            self.idx += 1
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="tag1",
                name="vector_search",
                response_time=total_time,
                response_length=len(str(res)),
            )
            # print(f"\nQuery: {raw_query}\nResult: {res}\n=========================")

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            print("\n===========================================================================")
            print(f"Exception: {e}")
            events.request.fire(
            # events.user_error.fire(
                request_type="tag1",
                name="vector_search",
                response_time=total_time,
                response_length=0,
                exception=str(e),
            )

    @tag("tag2")
    @task
    def similarity_search_2(self):
        start_time = time.time()
        
        try:
            if self.idx > 6_000_000:
                10/0
            
            res = 1+1
            self.idx += 1
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="tag2",
                name="vector_search",
                response_time=total_time,
                response_length=len(str(res)),
            )

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            print("\n===========================================================================")
            print(f"Exception: {e}")
            events.request.fire(
                request_type="tag2",
                name="vector_search",
                response_time=total_time,
                response_length=0,
                exception=str(e),
            )


# locuast --tags tag1 tag2