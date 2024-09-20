import aiohttp
import asyncio
import random
import logging
from aiohttp_socks import ProxyConnector
import aiofiles
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, tor_manager, config):
        self.proxies = []
        self.tor_manager = tor_manager
        self.config = config
        self.proxy_check_url = 'http://httpbin.org/ip'
        self.proxy_sources = [
            'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
        ]
        self.proxy_rotation_interval = timedelta(minutes=30)
        self.last_rotation_time = datetime.now()
        self.last_used_proxy = None
        self.consecutive_uses = 0
        self.max_consecutive_uses = 3

    async def update_proxies(self):
        try:
            tasks = [self.fetch_proxies(source) for source in self.proxy_sources]
            proxy_lists = await asyncio.gather(*tasks)
            self.proxies = [proxy for sublist in proxy_lists for proxy in sublist]
            logger.info(f"{len(self.proxies)} proxy güncellendi.")
            await self.validate_proxies()
            await self.save_proxies()
        except Exception as e:
            logger.error(f"Proxy güncellenirken hata oluştu: {e}")

    async def fetch_proxies(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                proxy_list = await response.text()
                return [{'http': f'http://{proxy}', 'https': f'https://{proxy}'} for proxy in proxy_list.split('\n') if proxy]

    async def validate_proxies(self):
        valid_proxies = []
        tasks = [self.check_proxy(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks)
        self.proxies = [proxy for proxy, is_valid in zip(self.proxies, results) if is_valid]
        logger.info(f"{len(self.proxies)} geçerli proxy bulundu.")

    async def check_proxy(self, proxy):
        try:
            connector = ProxyConnector.from_url(proxy['http'])
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(self.proxy_check_url, timeout=10) as response:
                    if response.status == 200:
                        return True
        except:
            pass
        return False

    async def get_proxy(self):
        if self.consecutive_uses >= self.max_consecutive_uses or not self.last_used_proxy:
            if random.random() < self.config.tor_probability:
                proxy = await self.tor_manager.get_tor_proxy()
            else:
                proxy = random.choice(self.proxies)
            self.last_used_proxy = proxy
            self.consecutive_uses = 1
        else:
            proxy = self.last_used_proxy
            self.consecutive_uses += 1
        
        return proxy

    async def rotate_proxies(self):
        await self.update_proxies()
        self.last_rotation_time = datetime.now()
        logger.info("Proxy'ler yenilendi.")

    async def rotate_ip(self):
        if isinstance(self.last_used_proxy, dict) and 'tor' in self.last_used_proxy:
            await self.tor_manager.renew_tor_ip()
        else:
            self.last_used_proxy = None
            self.consecutive_uses = 0

    async def save_proxies(self):
        async with aiofiles.open('valid_proxies.json', mode='w') as f:
            await f.write(json.dumps(self.proxies))

    async def load_proxies(self):
        try:
            async with aiofiles.open('valid_proxies.json', mode='r') as f:
                content = await f.read()
                self.proxies = json.loads(content)
        except FileNotFoundError:
            logger.warning("Kayıtlı proxy listesi bulunamadı.")