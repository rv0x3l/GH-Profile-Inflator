import asyncio
import aiohttp
import random
from aiohttp_proxy import ProxyConnector

TARGET_URL = "https://komarev.com/ghpvc/?username=rv0x3l&color=green"
CONCURRENT_REQUESTS = 50
PROXIES_FILE = "proxies.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def load_proxies():
    try:
        with open(PROXIES_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

async def hit(proxy):
    connector = ProxyConnector.from_url(proxy)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Cache-Control": "no-cache"
    }
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(TARGET_URL, headers=headers, timeout=15) as resp:
                print(f"[{resp.status}] {proxy}")
    except:
        pass

async def main():
    proxies = load_proxies()
    if not proxies:
        return

    tasks = []
    while True:
        for p in proxies:
            p_url = p if p.startswith("http") else f"http://{p}"
            tasks.append(asyncio.create_task(hit(p_url)))
            if len(tasks) >= CONCURRENT_REQUESTS:
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
      
