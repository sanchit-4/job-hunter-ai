import asyncio
from langchain.tools import tool
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class ScrapingEngine:
    @staticmethod
    async def extract_text_from_url(url: str):
        async with async_playwright() as p:
            # Launch headless browser (stealth mode recommended for real use)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            try:
                await page.goto(url, timeout=30000)
                # Wait for content to load
                await page.wait_for_load_state("networkidle")
                content = await page.content()
                
                # Parse with BS4 to reduce token count for LLM
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove scripts and styles
                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()
                    
                text = soup.get_text(separator="\n")
                return text[:8000] # Truncate to avoid context window overflow
            except Exception as e:
                return f"Error scraping {url}: {str(e)}"
            finally:
                await browser.close()

@tool
async def scrape_job_description(url: str) -> str:
    """Useful for extracting job requirements from a specific job posting URL."""
    return await ScrapingEngine.extract_text_from_url(url)