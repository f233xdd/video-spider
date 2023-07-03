import functools
import time
from threading import Lock, Thread


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


class CountTimeThread(Thread):
    _sign_time = time.perf_counter

    def __init__(self, target, name, args, kwargs):
        super().__init__(target=target, name=name, args=args, kwargs=kwargs)
        self.delta_t = None

    @classmethod
    def set_counter(cls, func):
        cls._sign_time = func

    def run(self) -> None:
        t1 = self._sign_time()
        super().run()
        t2 = self._sign_time()
        self.delta_t = t2 - t1


def runtime(func, *args, times=8, count_sleep=True, **kwargs):
    if not count_sleep:
        CountTimeThread.set_counter(time.process_time)

    threads = [CountTimeThread(target=func, name=f"Thread-{i}", args=args, kwargs=kwargs) for i in range(times)]
    for thd in threads:
        thd.start()
    for thd in threads:
        thd.join()

    total = 0
    for thread in threads:
        total += thread.delta_t

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
