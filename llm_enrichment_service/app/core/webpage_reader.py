from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup
import asyncio
import logging
async def read_webpage(url:str):
    TIMEOUT=60000
    async with async_playwright() as p:
        try:
            browser=await p.chromium.launch(headless=True)
            context=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
            page=await context.new_page()
            await stealth_async(page)
            await page.goto(url, timeout=TIMEOUT, wait_until="networkidle")
            content=await page.content()
            soup=BeautifulSoup(content, "html.parser")
            for element in soup(['style', 'script']):
                element.decompose()
            body=soup.body
            if body is None:
                raise ValueError("Body element not found")
            for tag in body.find_all():
                for key in list(tag.attrs):
                    del tag.attrs[key]
            return str(body)
        except Exception as e:
            logging.error(f"Error occured reading {url}:{e}")
            return None
        finally:
            await context.close()
            

# TEST
url="https://www.visitlondon.com/things-to-do/whats-on/special-events/london-events-calendar"
html=asyncio.run(read_webpage(url))
print(html)
if html is not None:
    with open("vist_london.html", "w") as f:
        f.write(html)