import aiohttp
from bs4 import BeautifulSoup
import asyncio
import logging
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from tenacity import retry, stop_after_attempt, wait_random
from pyppeteer import launch
import random
from urllib.parse import urlparse, urljoin
import tldextract
import js2py
import aiofiles
import hashlib
from stealth_utils import add_human_behavior, randomize_viewport, add_browser_fingerprint_evasion, add_canvas_fingerprint_evasion, add_webgl_fingerprint_evasion, add_advanced_fingerprint_evasion, AIBehaviorSimulator, MLProxyRotator
from user_agents import parse
import ssl
import certifi
import esprima
import jsbeautifier
from content_analyzer import ContentAnalyzer

logger = logging.getLogger(__name__)

class AsyncScraper:
    def __init__(self, proxy_manager, data_manager, captcha_solver, config):
        self.proxy_manager = proxy_manager
        self.data_manager = data_manager
        self.captcha_solver = captcha_solver
        self.config = config
        self.ua = UserAgent()
        self.session = None
        self.visited_urls = set()
        self.url_patterns = []
        self.ai_behavior_simulator = AIBehaviorSimulator()
        self.ml_proxy_rotator = MLProxyRotator()
        self.user_agents = self.load_user_agents()
        self.content_analyzer = ContentAnalyzer()

    async def create_session(self):
        ssl_context = create_ssl_context()
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))

    async def close_session(self):
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=3))
    async def scrape(self, url, depth=0):
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        proxy = await self.proxy_manager.get_proxy()
        headers = self.get_headers()

        if self.config.use_js_rendering:
            content = await self.render_js(url, proxy)
        else:
            content = await self.fetch_content(url, proxy, headers)

        soup = BeautifulSoup(content, 'lxml')

        if await self.detect_honeypot(soup):
            logger.warning(f"Honeypot tespit edildi: {url}")
            return None

        if self.captcha_solver.detect_captcha(soup):
            captcha_solution = await self.captcha_solver.solve(soup)
            content = await self.submit_captcha(url, captcha_solution, proxy, headers)
            soup = BeautifulSoup(content, 'lxml')

        data = await self.extract_data(soup, url)
        
        if data:
            analysis = self.content_analyzer.analyze(data['text'])
            data['analysis'] = analysis

        await self.follow_links(soup, url, depth)
        await self.human_like_delay()
        return data

    async def fetch_content(self, url, proxy, headers):
        connector = ProxyConnector.from_url(proxy['http'])
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Hata: {response.status} - {url}")
                    raise Exception(f"HTTP error {response.status}")

    async def render_js(self, url, proxy):
        browser = await launch(
            headless=True,
            args=['--no-sandbox', f'--proxy-server={proxy["http"]}', '--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
        )
        page = await browser.newPage()
        await page.setUserAgent(self.ua.random)
        await page.setJavaScriptEnabled(True)
        
        if self.config.use_stealth_mode:
            randomize_viewport(page)
            await add_browser_fingerprint_evasion(page)
            await add_canvas_fingerprint_evasion(page)
            await add_webgl_fingerprint_evasion(page)
            human_behavior = await add_human_behavior(page)
            await page.evaluateOnNewDocument(human_behavior)

        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
        
        # JavaScript analizi ve manipülasyonu
        await self.analyze_and_manipulate_js(page)
        
        if self.config.use_stealth_mode:
            await human_behavior()

        content = await page.content()
        await browser.close()
        return content

    async def analyze_and_manipulate_js(self, page):
        # Sayfadaki tüm script etiketlerini bulun
        scripts = await page.querySelectorAll('script')
        
        for script in scripts:
            # Script içeriğini alın
            js_content = await page.evaluate('(element) => element.innerHTML', script)
            
            if js_content:
                # JavaScript kodunu analiz edin
                try:
                    parsed = esprima.parseScript(js_content)
                    
                    # Anti-bot kontrolleri için anahtar kelimeler
                    anti_bot_keywords = ['bot', 'crawler', 'spider', 'headless', 'selenium', 'webdriver']
                    
                    # Anti-bot kontrollerini tespit edin ve manipüle edin
                    for node in parsed.body:
                        if node.type == 'IfStatement':
                            condition = node.test
                            if any(keyword in esprima.generate(condition) for keyword in anti_bot_keywords):
                                # Anti-bot kontrolünü devre dışı bırakın
                                modified_js = js_content.replace(esprima.generate(node), '')
                                
                                # Değiştirilmiş JavaScript'i sayfaya enjekte edin
                                await page.evaluate(f"""
                                    document.currentScript.innerHTML = `{modified_js}`;
                                    {modified_js}
                                """)
                                
                                logger.info(f"Anti-bot kontrolü tespit edildi ve devre dışı bırakıldı.")
                
                except Exception as e:
                    logger.error(f"JavaScript analizi sırasında hata oluştu: {e}")

    def get_headers(self):
        user_agent = random.choice(self.user_agents)
        parsed_ua = parse(user_agent)
        return {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Viewport-Width': str(random.randint(1024, 1920)),
            'Device-Memory': f'{random.randint(2, 8)}',
            'Referer': 'https://www.google.com/'
        }

    async def extract_data(self, soup, url):
        for pattern in self.url_patterns:
            if pattern['regex'].match(url):
                return pattern['extractor'](soup)
        return None

    async def submit_captcha(self, url, captcha_solution, proxy, headers):
        # Implement captcha submission logic here
        pass

    async def follow_links(self, soup, base_url, depth):
        if depth >= self.config.max_depth:
            return

        links = soup.find_all('a', href=True)
        base_domain = tldextract.extract(base_url).domain
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            if tldextract.extract(full_url).domain == base_domain:
                if random.random() < self.config.link_follow_probability:
                    await asyncio.sleep(random.uniform(self.config.min_delay, self.config.max_delay))
                    await self.scrape(full_url, depth + 1)

    async def execute_js(self, js_code):
        return js2py.eval_js(js_code)

    async def load_url_patterns(self):
        async with aiofiles.open('url_patterns.json', mode='r') as f:
            content = await f.read()
            self.url_patterns = json.loads(content)

    def fingerprint_page(self, content):
        return hashlib.md5(content.encode()).hexdigest()

    def get_site_features(self, url):
        # URL'den site özelliklerini çıkarın
        # Bu, projenizin spesifik gereksinimlerine göre uyarlanmalıdır
        pass

    async def detect_honeypot(self, soup):
        honeypot_indicators = [
            'trap', 'honeypot', 'spider', 'crawler',
            lambda tag: tag.has_attr('style') and 'display:none' in tag['style'].lower(),
            lambda tag: tag.has_attr('class') and any('hidden' in c.lower() for c in tag['class'])
        ]
        
        for indicator in honeypot_indicators:
            if callable(indicator):
                if soup.find_all(indicator):
                    return True
            else:
                if soup.find_all(string=lambda text: indicator in text.lower()):
                    return True
        return False

    async def human_like_delay(self):
        # Gaussian dağılımı kullanarak daha doğal gecikmeler oluşturun
        delay = np.random.normal(loc=2, scale=0.5)
        delay = max(0.5, min(delay, 5))  # 0.5 ile 5 saniye arasında sınırla
        await asyncio.sleep(delay)

    async def scrape(self, url, depth=0):
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        proxy = await self.proxy_manager.get_proxy()
        headers = self.get_headers()

        if self.config.use_js_rendering:
            content = await self.render_js(url, proxy)
        else:
            content = await self.fetch_content(url, proxy, headers)

        soup = BeautifulSoup(content, 'lxml')

        if await self.detect_honeypot(soup):
            logger.warning(f"Honeypot tespit edildi: {url}")
            return None

        if self.captcha_solver.detect_captcha(soup):
            captcha_solution = await self.captcha_solver.solve(soup)
            content = await self.submit_captcha(url, captcha_solution, proxy, headers)
            soup = BeautifulSoup(content, 'lxml')

        data = await self.extract_data(soup, url)
        
        if data:
            analysis = self.content_analyzer.analyze(data['text'])
            data['analysis'] = analysis

        await self.follow_links(soup, url, depth)
        await self.human_like_delay()
        return data