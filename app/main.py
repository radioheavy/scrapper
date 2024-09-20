import asyncio
import logging
from scraper import AsyncScraper
from proxy_manager import ProxyManager
from data_manager import DataManager
from app.captcha_solver import CaptchaSolver
from tor_manager import TorManager
from config import Config
import signal
import sys
from aiolimiter import AsyncLimiter
from distributed_scraper import DistributedScraper
from dashboard import app, socketio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='scraper.log', filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

async def main():
    config = Config()
    tor_manager = TorManager(config)
    proxy_manager = ProxyManager(tor_manager, config)
    data_manager = DataManager(config.encryption_key)
    captcha_solver = CaptchaSolver(config.captcha_api_key, config.captcha_model_path)
    
    if config.use_distributed_scraping:
        scraper = DistributedScraper(proxy_manager, data_manager, captcha_solver, config)
        await scraper.distribute_tasks(config.target_urls)
        await DistributedScraper.run_workers(config.num_workers, proxy_manager, data_manager, captcha_solver, config)
    else:
        scraper = AsyncScraper(proxy_manager, data_manager, captcha_solver, config)
        await tor_manager.start()
        await proxy_manager.update_proxies()
        await scraper.create_session()

        urls = config.target_urls
        rate_limiter = AsyncLimiter(config.max_concurrent_requests)

        def signal_handler(sig, frame):
            logger.info('Scraping işlemi kullanıcı tarafından durduruldu.')
            asyncio.create_task(cleanup())

        signal.signal(signal.SIGINT, signal_handler)

        async def cleanup():
            await scraper.close_session()
            await tor_manager.stop()
            sys.exit(0)

        try:
            async def limited_scrape(url):
                async with rate_limiter:
                    return await scraper.scrape(url)

            tasks = [limited_scrape(url) for url in urls]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    await data_manager.save(result)
        except Exception as e:
            logger.error(f"Ana döngüde hata oluştu: {e}")
        finally:
            if config.use_distributed_scraping:
                await scraper.run()
            else:
                await cleanup()

if __name__ == "__main__":
    socketio.start_background_task(target=asyncio.run, args=(main(),))
    socketio.run(app, debug=True)