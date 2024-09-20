from setuptools import setup, find_packages

setup(
    name="advanced-web-scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        aiohttp==3.8.4
aiohttp-socks==0.7.1
aiofiles==0.8.0
aioredis==2.0.1
asyncio==3.4.3
beautifulsoup4==4.10.0
cryptography==3.4.7
fake-useragent==0.1.11
js2py==0.71
lxml==4.6.3
pyppeteer==0.2.6
python-dotenv==0.19.0
requests==2.26.0
stem==1.8.0
tenacity==8.0.1
tldextract==3.1.2
twocaptcha-python==1.0.3
    ],
)