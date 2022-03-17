from concurrent.futures import ThreadPoolExecutor
import threading
import time
from bs4 import BeautifulSoup
import requests
import queue
import asyncio
import aiohttp


def get_web_page_title(link, q):
    resp = requests.get(link)
    bs = BeautifulSoup(resp.content, 'html.parser')
    q.put(bs.title.string)


def task_in_sync(web_links):
    t1 = time.time()
    print("Program running in synchronous manner")
    titles = queue.Queue()

    for wl in web_links:
        get_web_page_title(wl, titles)
    print(list(titles.queue))

    t2 = time.time()
    print("Time taken: ", t2-t1)


def task_in_multi_thread(web_links):
    t1 = time.time()
    print("\nProgram running in multi threading manner")
    titles = queue.Queue()
    threads = []
    for wl in web_links:
        thread = threading.Thread(target=get_web_page_title, args=(wl, titles))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(list(titles.queue))
    t2 = time.time()
    print("Time taken: ", t2-t1)


def task_in_thread_pool(web_links):
    t1 = time.time()
    print("\nProgram running in thread pool executor")
    titles = queue.Queue()
    with ThreadPoolExecutor(max_workers=3) as executor:
        # for wl in web_links:
        #     executor.submit(get_web_page_title, wl, titles)
        executor.map(get_web_page_title, web_links, (titles, titles, titles))
    print(list(titles.queue))
    t2 = time.time()
    print("Time taken: ", t2-t1)


async def async_get_web_page_title(link, q):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            bs = BeautifulSoup(await response.content.read(), 'html.parser')
            q.put(bs.title.string)


async def task_in_async(web_links):
    t1 = time.time()
    print("\nProgram running in thread pool executor")
    titles = queue.Queue()
    await asyncio.gather(*(async_get_web_page_title(wl, titles) for wl in web_links))
    print(list(titles.queue))
    t2 = time.time()
    print("Time taken: ", t2-t1)


def main():
    web_links = ["https://python.org",
                 "https://www.perl.org", "https://go.dev"]
    task_in_sync(web_links)
    task_in_multi_thread(web_links)
    task_in_thread_pool(web_links)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_in_async(web_links))


if __name__ == "__main__":
    main()
