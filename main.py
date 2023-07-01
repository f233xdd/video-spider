import asyncio
import threading

import spider


async def main():
    base = "HERE!"
    spider.Spider.set_url(base)

    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, spider.Downloader(f"Downloader({i})").get_data) for i in
               range(1, 11)]

    threading.Thread(target=spider.Writer("Writer(Main)").write).start()
    await asyncio.gather(*futures)


if __name__ == "__main__":
    asyncio.run(main())
