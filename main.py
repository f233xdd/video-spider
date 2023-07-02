import asyncio

from spider import main


if __name__ == "__main__":
    base = "https://vip.lz-cdn14.com/20221210/16181_062349e7/2000k/hls/ca9cd59ecd0@@@@@@.ts"
    asyncio.run(main(base, 15))
