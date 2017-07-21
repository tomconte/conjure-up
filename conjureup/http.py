import asyncio
import aiohttp

class HTTPClient:
    def __init__(self):
        pass

    async def get(self, url):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as resp:
                return await resp.json()

    async def get(self, url):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as resp:
                return await resp.json()
