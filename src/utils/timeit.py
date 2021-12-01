import time
from functools import wraps


def timeit(timed_function):
    @wraps(timed_function)
    def timer(*args, **kwargs):
        time_before = time.time()
        print(f"Timing function: {timed_function.__name__}.")
        result = timed_function(*args, **kwargs)
        elapsed = round((time.time() - time_before), 4)
        print(f"Arguments: [{args}, {kwargs}]")
        print(f"The job took {elapsed} seconds to complete.")
        return result

    return timer
