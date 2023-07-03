import functools
import time
from threading import Lock


def counter(debug=True):
    """Calculate and print the process time of a function, including sleeping times."""

    def check_debug_option(func):
        @functools.wraps(func)
        def count_process_time(*args, **kwargs):
            time1 = time.perf_counter()
            value = func(*args, **kwargs)
            time2 = time.perf_counter()
            if debug:
                print(f"[Process--function({func.__name__})]({round(time2 - time1, 3)} secs)")
            return value

        return count_process_time

    return check_debug_option


def start_and_exit_sign(debug=True):
    """Print when a function start and exit dynamically in your terminal."""

    def check_debug_option(func):
        @functools.wraps(func)
        def mark_start_and_exit(*args, **kwargs):
            if debug:
                print(f"########Start({func.__name__})########")
            value = func(*args, **kwargs)
            if debug:
                print(f"########Exit({func.__name__})########")
            return value

        return mark_start_and_exit

    return check_debug_option


def runtime(func, times=8, count_sleep=True, *args, **kwargs):
    if count_sleep:
        sign_time = time.perf_counter
    else:
        sign_time = time.process_time

    process_time = []
    for i in range(times):
        t1 = sign_time()
        func(*args, **kwargs)
        t2 = sign_time()
        process_time.append((t1, t2, t2 - t1))

    n = 0
    total = 0
    for t1, t2, delta_t in process_time:
        print(f"Process_{n}: ({t1}s, {t2}s)")
        total += delta_t
        n += 1

    average = total / times
    print(f"Average run time: {average}")


l = Lock()


def mark(n):
    d = {1: "FST",
         2: "SEC",
         3: "TRD",
         4: "FOR",
         5: "FIF",
         }

    with l:
        print(f"====================Mark Point[{d[n]}]====================")
