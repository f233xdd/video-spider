import debug
import time


def sp(t, s=None):
    print(s)
    time.sleep(t)


debug.runtime(sp, 3, times=100, s="qwq")
