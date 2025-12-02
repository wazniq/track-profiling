from playwright.sync_api import sync_playwright
import pandas as pd
import os

EXCEL_FILE = 'Test.xlsx'
START_URL = 'https://ircep.gov.in/TMS/HomeIframe.jsp'
USER_DATA_DIR = os.path.abspath("chrome_profile")

def run():
    # 1. Read Excel Data
    print("Reading Excel file...")
    try:
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl', header=[0, 1])
        print("Excel file read successfully.")
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    with sync_playwright() as p:
        print("Launching Chrome with persistent profile...")
        # Use launch_persistent_context to keep cookies/cache and look more 'real'
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                channel="chrome",
                viewport=None, # specific for persistent context to not override window size
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
            )
        except Exception as e:
            print(f"Error launching persistent context: {e}")
            print("Please ensure no other Chrome instances are using this profile directory.")
            return

        # Get the initial page
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = browser.new_page()

        print(f"Navigating to {START_URL}...")
        try:
            page.goto(START_URL)
        except Exception as e:
            print(f"Navigation error: {e}")

        print("\n" + "="*50)
        print("ACTION REQUIRED: Log in and navigate to the Data Entry Form.")
        print("If a new window opens, I will try to detect it.")
        print("When you are ready to start entering data, press ENTER in this terminal.")
        print("="*50 + "\n")
        
        input("Press Enter to start data entry...")

        # Get the active page (likely the last one opened/focused)
        # In persistent context, pages are managed directly on the context object
        pages = browser.pages
        target_page = pages[-1] 
        print(f"Targeting page: {target_page.title()} ({target_page.url})")

        print("Automation ready to proceed. (Logic to be implemented)")
        # input("Press Enter to close...")

if __name__ == "__main__":
    run()
