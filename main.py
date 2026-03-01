import json
import asyncio
import sys
import argparse
import os
from playwright.async_api import async_playwright

async def run_debugger(url_to_debug, config_path):
    if not os.path.exists(config_path):
        print(f"Error: Config file {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)
    
    cookies = config.get('cookies', [])
    if not cookies:
        print("Warning: No cookies found in config. Automation might fail due to login requirements.")

    async with async_playwright() as p:
        # Launching with headless=True as it's for console automation. 
        # If user wants to see it, they can change to False.
        browser = await p.chromium.launch(headless=True) 
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        # Add cookies to the context
        if cookies:
            # Playwright expects sameSite to be Strict, Lax, or None
            for cookie in cookies:
                if 'sameSite' in cookie:
                    ss = cookie['sameSite'].lower()
                    if ss == 'no_restriction':
                        cookie['sameSite'] = 'None'
                    elif ss in ['strict', 'lax', 'none']:
                        cookie['sameSite'] = ss.capitalize()
                    else:
                        # Default to None if unknown, as it's the safest for automation
                        cookie['sameSite'] = 'None'
                
                # Remove fields that might not be supported or are null
                if 'storeId' in cookie and cookie['storeId'] is None:
                    del cookie['storeId']

            await context.add_cookies(cookies)
        
        page = await context.new_page()
        print(f"Navigating to Facebook Debugger...")
        try:
            await page.goto("https://developers.facebook.com/tools/debug/", wait_until="domcontentloaded")
        except Exception as e:
            print(f"Error loading page: {e}")
            await browser.close()
            return
        
        # 1. Enter URL
        print(f"Entering URL: {url_to_debug}")
        # Trying multiple selectors for the input field
        url_input = page.locator('input[placeholder*="Introduce una URL"], input[type="text"], input#u_0_1_fb').first
        await url_input.fill(url_to_debug)
        
        # 2. Click Debug (Depurar)
        print("Clicking 'Depurar'...")
        # Search for button with text "Depurar"
        debug_button = page.get_by_role("button", name="Depurar", exact=True)
        await debug_button.click()
        
        # Wait for results page to load
        print("Waiting for results...")
        try:
            await page.wait_for_load_state("load", timeout=15000)
        except Exception:
            print("Wait for 'load' state timed out, proceeding anyway...")
        
        # 3. Check for 'Volver a extraer' (Scrape Again)
        try:
            # We look for the button that says "Volver a extraer"
            scrape_again_button = page.get_by_role("button", name="Volver a extraer", exact=True)
            if await scrape_again_button.is_visible(timeout=5000):
                print("Found 'Volver a extraer'. Clicking it to ensure fresh data...")
                await scrape_again_button.click()
                try:
                    await page.wait_for_load_state("load", timeout=10000)
                except Exception:
                    pass
                print("Scrape refreshed successfully.")
            else:
                print("'Volver a extraer' button not visible.")
        except Exception:
            print("Note: 'Volver a extraer' button not found.")
            
        # Final Verification: Extract results
        results = {}
        try:
            # 1. Extraction Time
            extraction_time_label = page.get_by_text("Tiempo de extracción").first
            if await extraction_time_label.is_visible():
                # Get the cell containing the time
                row = extraction_time_label.locator("xpath=./ancestor::tr")
                # The value is usually in the second TD
                value_td = row.locator("td").nth(1)
                if await value_td.is_visible():
                    raw_text = await value_td.inner_text()
                    # Clean up "Volver a extraer" if present
                    results['extraction_time'] = raw_text.replace("Volver a extraer", "").strip()
                    print(f"Extraction Time: {results['extraction_time']}")
            
            # 2. Preview Title, Description & Image
            # Look for the container that has the preview
            preview_container = page.locator("div._4-u2._4-u8").filter(has_text="Vista previa del enlace").first
            if not await preview_container.is_visible():
                preview_container = page.locator("div:has(> img)").filter(has_text="LNE.ES").first # Specific to this test but generic idea

            # Search Title
            title_el = page.locator("div._642e, ._3naw, h3").first
            if await title_el.is_visible():
                results['title'] = await title_el.inner_text()
                print(f"Preview Title: {results['title']}")
            
            # Search Description
            desc_el = page.locator("div._642f, div._2swm").first
            if await desc_el.is_visible():
                results['description'] = await desc_el.inner_text()
                print(f"Preview Description: {results['description']}")
            
            # Search Image (if not already found)
            if 'image_url' not in results:
                img_el = page.locator("div._4-u2 img").first
                if await img_el.is_visible():
                    results['image_url'] = await img_el.get_attribute("src")
                    print(f"Preview Image URL: {results['image_url']}")

            # 3. Warnings
            warnings_el = page.locator("div._4-u2").filter(has_text="Advertencias que deberían solucionarse").first
            if await warnings_el.is_visible():
                results['warnings'] = (await warnings_el.inner_text()).replace("Advertencias que deberían solucionarse", "").strip()
                print(f"Warnings Found: {results['warnings'][:100]}...")

            if not results:
                print("Warning: Could not extract specific results.")
                
        except Exception as e:
            print(f"Could not verify status text: {e}")

        # Screenshot for the user to see the result
        screenshot_path = "facebook_debug_result.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Automation complete. Screenshot saved as {screenshot_path}")
        
        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook Debugger Automation')
    parser.add_argument('url', help='The URL to debug (e.g., https://www.lne.es/)')
    parser.add_argument('--config', default='config_facebook_developer.json', help='Path to config file')
    
    args = parser.parse_args()
    
    if not args.url.startswith('http'):
        print("Error: Please provide a full URL starting with http:// or https://")
        sys.exit(1)
        
    asyncio.run(run_debugger(args.url, args.config))
