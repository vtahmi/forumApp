import time


def measure_execution_time(func):
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        result = func(request, *args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        return result
    return wrapper

@measure_execution_time
def sum(a, b):
    return a + b

sum(1, 2)