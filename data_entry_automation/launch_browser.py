from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        print("Launching Google Chrome...")
        # Try to launch Google Chrome specifically
        try:
            browser = p.chromium.launch(headless=False, channel="chrome")
        except Exception as e:
            print(f"Could not launch Chrome: {e}")
            print("Falling back to standard Chromium...")
            browser = p.chromium.launch(headless=False)

        context = browser.new_context(viewport=None) # Disable viewport emulation to look more 'native'
        page = context.new_page()
        
        print("Browser launched. Please navigate to the login page and log in.")
        print("Once you are on the target form page, press Enter here to continue...")
        
        # Keep the script running until user presses Enter
        input()
        
        print("Continuing automation... (This is where the data entry logic will go)")
        
        # Keep browser open for now so we can inspect if needed, or close if script ends
        # For the actual automation, we will continue from here.
        # browser.close() 

if __name__ == "__main__":
    run()
