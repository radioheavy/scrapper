import asyncio
import aioredis
from scraper import AsyncScraper
import json

class DistributedScraper(AsyncScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = None

    async def connect_redis(self):
        self.redis = await aioredis.create_redis_pool(self.config.redis_url)

    async def disconnect_redis(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()

    async def get_task(self):
        return await self.redis.blpop('scrape_tasks', timeout=1)

    async def add_task(self, url):
        await self.redis.rpush('scrape_tasks', url)

    async def save_result(self, result):
        await self.redis.rpush('scrape_results', json.dumps(result))

    async def run(self):
        await self.connect_redis()
        while True:
            task = await self.get_task()
            if not task:
                continue
            _, url = task
            result = await self.scrape(url.decode())
            if result:
                await self.save_result(result)
        await self.disconnect_redis()

    async def distribute_tasks(self, urls):
        for url in urls:
            await self.add_task(url)

    @classmethod
    async def create_worker(cls, *args, **kwargs):
        worker = cls(*args, **kwargs)
        await worker.create_session()
        return worker

    @classmethod
    async def run_workers(cls, num_workers, *args, **kwargs):
        workers = [await cls.create_worker(*args, **kwargs) for _ in range(num_workers)]
        await asyncio.gather(*(worker.run() for worker in workers))