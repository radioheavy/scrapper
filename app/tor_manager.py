import asyncio
from stem import Signal
from stem.control import Controller
import logging

logger = logging.getLogger(__name__)

class TorManager:
    def __init__(self, config):
        self.config = config
        self.controller = None

    async def start(self):
        try:
            self.controller = Controller.from_port(port=self.config.tor_control_port)
            await asyncio.to_thread(self.controller.authenticate)
            logger.info("Tor kontrolcüsü başlatıldı.")
        except Exception as e:
            logger.error(f"Tor başlatılırken hata oluştu: {e}")

    async def stop(self):
        if self.controller:
            await asyncio.to_thread(self.controller.close)
        logger.info("Tor durduruldu.")

    async def renew_tor_ip(self):
        try:
            await asyncio.to_thread(self.controller.signal, Signal.NEWNYM)
            logger.info("Yeni Tor IP alındı.")
        except Exception as e:
            logger.error(f"Tor IP yenilenirken hata oluştu: {e}")

    async def get_tor_proxy(self):
        await self.renew_tor_ip()
        return {'http': f'socks5://localhost:{self.config.tor_port}', 
                'https': f'socks5://localhost:{self.config.tor_port}'}