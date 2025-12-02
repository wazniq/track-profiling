from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        print("Connecting to Chrome on port 9222...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"Connection failed: {e}")
            return

        context = browser.contexts[0]
        # Find the likely target page (the one with 'TMS' or 'Inspection' or just the active one)
        target_page = None
        
        # Simple heuristic: Last opened page or page with specific URL
        if context.pages:
            target_page = context.pages[-1]
            print(f"Targeting page: {target_page.title()} ({target_page.url})")
        else:
            print("No pages found.")
            return

        # Dump HTML to file
        print("Dumping HTML...")
        try:
            # Wait a bit for any frames to load
            target_page.wait_for_load_state("domcontentloaded")
            content = target_page.content()
            
            # Also try to get content of iframes if any
            frames_content = ""
            for frame in target_page.frames:
                try:
                    frames_content += f"\n\n<!-- FRAME: {frame.name} -->\n"
                    frames_content += frame.content()
                except:
                    pass
            
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(content + frames_content)
            print("HTML saved to page_dump.html")
        except Exception as e:
            print(f"Error dumping HTML: {e}")

if __name__ == "__main__":
    run()
