import asyncio
from playwright.async_api import async_playwright

async def get_portal_intelligence(url, user=None, pw=None):
    """
    RRIS Universal Crawler 2.0
    One script to rule them all: Handle logins, scrape content, and clean text.
    """
    async with async_playwright() as p:
        # 1. Setup Browser with 'Human' Fingerprint
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"📡 Deep-scanning portal: {url}")
            # Increase timeout for slow recruiter portals
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # 2. SMART LOGIN (Only if credentials provided)
            if user and pw:
                print("🔑 Attempting Universal Login...")
                try:
                    # Look for anything that looks like an email/user field
                    user_selector = "input[type='email'], input[type='text'], input[name*='user'], input[name*='login']"
                    pass_selector = "input[type='password']"
                    
                    # Wait briefly for fields to appear
                    await page.wait_for_selector(user_selector, timeout=5000)
                    
                    await page.locator(user_selector).first.fill(user)
                    await page.locator(pass_selector).first.fill(pw)
                    await page.keyboard.press("Enter")
                    
                    # Wait for the dashboard to actually load after login
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    print("✅ Login sequence completed.")
                except Exception as login_err:
                    print(f"⚠️ Login skipped/failed (likely already logged in or custom flow): {login_err}")

            # 3. CONTENT EXTRACTION
            # We wait for the 'body' to be stable
            await page.wait_for_load_state("networkidle")
            
            # Extract only visible text (removes <script>, <style>, and HTML tags)
            raw_text = await page.evaluate("() => document.body.innerText")
            
            # 4. DATA CLEANING
            # Remove excessive newlines and tabs to save AI tokens
            clean_text = " ".join(raw_text.split())
            
            # Return first 6000 chars (plenty for status and job details)
            return clean_text[:6000]

        except Exception as e:
            print(f"❌ Universal Crawler Error: {e}")
            return None
        finally:
            await browser.close()

# Example usage for your internal testing:
# if __name__ == "__main__":
#     content = asyncio.run(get_portal_intelligence("https://turing.com/dashboard", "user@email.com", "pass123"))
#     print(content)