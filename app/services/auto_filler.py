from playwright.async_api import async_playwright

async def fill_easy_apply(url: str, user_data: dict):
    """
    Experimental: Attempts to fill generic Greenhouse/Lever forms.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headless=False to see it working
        page = await browser.new_page()
        await page.goto(url)
        
        # Heuristic: Find inputs by label
        try:
            # First Name
            await page.get_by_label("First Name").fill(user_data['first_name'])
            # Last Name
            await page.get_by_label("Last Name").fill(user_data['last_name'])
            # Email
            await page.get_by_label("Email").fill(user_data['email'])
            
            # File Upload (Resume) - Assumes you generated a PDF earlier
            # await page.get_by_label("Resume").set_input_files("generated_resume.pdf")
            
            print("Form filled. Waiting for manual review...")
            await asyncio.sleep(60) # Keep browser open for user to click submit
            
        except Exception as e:
            print(f"Auto-fill failed: {e}")
        finally:
            await browser.close()