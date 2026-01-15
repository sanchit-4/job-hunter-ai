import asyncio
import random
import requests
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def clean_text_for_ai(text: str) -> str:
    # Remove multiple newlines and extra spaces
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fallback_scrape(url: str) -> str:
    print(f"⚠️ Switching to Fallback Scraper for {url}")
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Clean
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
            
        return clean_text_for_ai(soup.get_text(separator="\n"))[:15000]
    except Exception as e:
        print(f"Fallback failed: {e}")
        return ""

@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
async def scrape_job_text(url: str) -> str:
    try:
        async with async_playwright() as p:
            # Launch without headless first to debug if needed, or stick to True
            browser = await p.chromium.launch(headless=True)
            
            context = await browser.new_context(
                user_agent=random.choice(USER_AGENTS)
            )
            page = await context.new_page()
            
            try:
                print(f"Attempting Playwright scrape: {url}")
                await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                content = await page.content()
                
                soup = BeautifulSoup(content, "html.parser")
                for tag in soup(["script", "style", "nav", "footer"]):
                    tag.decompose()
                    
                text = clean_text_for_ai(soup.get_text(separator="\n"))
                
                if len(text) < 200:
                    raise Exception("Playwright content too short")
                    
                return text[:15000]
                
            except Exception as e:
                print(f"Playwright error: {e}")
                raise e # Trigger retry or fallback
            finally:
                await browser.close()
                
    except Exception:
        # If Playwright fails completely (e.g. Windows Loop Error), use fallback
        return fallback_scrape(url)