import debug
import time


def sp():
    print("qwq")
    time.sleep(5)


debug.runtime(sp, times=100)
