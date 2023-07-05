import asyncio
import sys
import queue
import threading
import typing

import requests
import filetools

from debug import *


class Spider(object):
    spiders = 0
    _queue = queue.Queue()
    _base_url = None
    _urls = None

    def __init__(self, name: str):
        self.name = name
        Spider.spiders += 1

    @classmethod
    def set_url(cls, base_url: str, start=0, stop=None):
        cls._base_url = base_url
        cls._urls = cls.__url_creator(start, stop)

    @classmethod
    def __url_creator(cls, start, stop) -> typing.Generator:
        i = start
        cls.start = start

        if stop is not None:
            sign = stop + 1
        else:
            sign = -1

        # TODO
        while i != sign:
            yield i, cls._base_url.replace('@@@@@@', f'{i:0>6}')
            i += 1

        # while i != sign:
        #     yield i, cls._base_url.replace('@', f"0{i}")
        #     i += 1


class Downloader(Spider):
    def __init__(self, name):
        super().__init__(name=name)

    def get_data(self):
        time_of_404 = 0
        priority = None
        lock = threading.Lock()

        while True:
            try:
                priority, url = next(self._urls)

                with lock:
                    page = requests.get(url=url, timeout=(3.05, 9))

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


class Writer(Spider):
    def __init__(self, name):
        super().__init__(name)

    def write(self):
        error_log = open('error.log', 'a')
        lock = threading.Lock()
        rest = list()
        current = self.start
        fd = filetools.DirFileManager(file='out.ts')

        while True:
            try:
                priority, data = self._queue.get(block=True, timeout=10)

                if priority == current:

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


class NetConnectionError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return str(f"<NetConnectionError[{self.status_code}]>")


async def main(base_url: str, downloaders: int = 5):
    downloaders += 1
    Spider.set_url(base_url)

    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, Downloader(f"Downloader({i})").get_data) for i in
               range(1, downloaders)]

    threading.Thread(target=Writer("Writer(Main)").write).start()
    print(Spider.spiders)
    await asyncio.gather(*futures)


if __name__ == "__main__":
    raise RuntimeError
