# unit test
import time

import debug
from spider import *


class TestSpider(Spider):

    def get_data(self):
        time_of_404 = 0
        priority = None
        lock = threading.Lock()
        while True:
            try:
                priority, url = next(self._urls)
                with lock:
                    page = requests.get(url=url, timeout=2)
                if page.status_code == 200:
                    self._queue.put((priority, page.content), block=True)  # 在队列中放入列表
                    print(f"Get: {url} | from {self.name}")
                else:
                    raise NetConnectionError(page.status_code)
            except NetConnectionError as e:
                print(f"Fail: {url} | {e} | from {self.name}")
                if e.status_code == 404:
                    time_of_404 += 1
                if time_of_404 == 2:
                    print(f"Exit[404]! | from {self.name}")
                    break
            except requests.exceptions.ReadTimeout:
                print(f"TimeOut!{url} | from {self.name}")
                self._queue.put((priority, None), block=True)
            except StopIteration:
                print(f"Exit! | from {self.name}")
                break

    def write(self):
        error_log = open('error.log', 'a')
        lock = threading.Lock()
        rest = list()
        current = self.start
        fd = filetools.DirFileManager(file='out.ts')

        while True:
            try:
                priority, data = self._queue.get(block=True, timeout=10)

                if data is None:
                    print(f"before {priority} {current}")

                if priority == current:

                    if data is None:
                        print(f"after {priority} {current}")

                    with lock:
                        if data is None:
                            fd.create_new_file()
                            error_log.write(f"{priority} cannot get.\n")
                            print(f"{priority} cannot get.\n")
                            current += 1
                        else:
                            fd.write(data)
                            print(f"Write data[{priority}] | from {self.name}")
                            current += 1
                else:
                    rest.append((priority, data))  # 如果获取的队列元素不合预期，就储存起来
                    rest.sort()
            except (TimeoutError, queue.Empty):
                print(f"TimeOut! | from {self.name}")
                error_log.close()
                sys.exit(10)
            index = 0
            while index != len(rest):  # 检查有没有符合预期的元素，有就写入数据
                if rest[index][0] == current:
                    i, msg = rest.pop(index)
                    fd.write(msg)
                    print(f"Write data[{i}] | from {self.name}")
                    current += 1
                    index -= 1
                index += 1


def l(t, s):
    print(s)
    time.sleep(t)


runtime(l, 3, times=5)
