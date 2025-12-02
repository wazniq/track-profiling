from playwright.sync_api import sync_playwright
import pandas as pd
import math

EXCEL_FILE = 'Test.xlsx'

def clean_value(val):
    if pd.isna(val):
        return "0"
    try:
        # User requested "rounded to the next whole number" -> Ceiling
        # e.g. 2.1 -> 3, 4.0 -> 4
        float_val = float(val)
        return str(math.ceil(float_val))
    except (ValueError, TypeError):
        return str(val)

def run():
    print("Reading Excel file...")
    try:
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl', header=[0, 1])
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    excel_data = {}
    for index, row in df.iterrows():
        station_val = row[('Station', 'No.')]
        if pd.isna(station_val):
            continue
        if isinstance(station_val, float) and station_val.is_integer():
            station_str = str(int(station_val))
        else:
            station_str = str(station_val)
        excel_data[station_str] = row

    with sync_playwright() as p:
        print("Connecting to Chrome on port 9222...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"Connection failed: {e}")
            return

        context = browser.contexts[0]
        
        # Find the correct page
        target_page = None
        print("Searching for Curve Inspection page...")
        for page in context.pages:
            title = page.title()
            url = page.url
            print(f"  Checking: {title} ({url})")
            if "Curve Inspection" in title or "CurveInspectionController" in url:
                target_page = page
                break
        
        if not target_page:
            print("ERROR: Could not find the 'Curve Inspection' page. Please make sure the form is open.")
            return
            
        print(f"Targeting page: {target_page.title()}")

        # Handle Dialogs
        target_page.on("dialog", lambda dialog: dialog.accept())

        print("Mapping form stations...")
        station_inputs = target_page.locator('input[name="station"]')
        count = station_inputs.count()
        print(f"Found {count} stations on the form.")

        if count == 0:
            print("No stations found. Is the page loaded correctly?")
            return

        for i in range(count):
            station_val = station_inputs.nth(i).evaluate("el => el.value")
            if not station_val:
                continue
            station_str = str(station_val).strip()
            print(f"Processing Station {station_str} (Row {i})...")
            
            if station_str in excel_data:
                row = excel_data[station_str]
                # Helper to safely get value from row
                def get_val(col_tuple):
                    if col_tuple in row.index:
                        return clean_value(row[col_tuple])
                    return "0" # Default if column missing in Excel

                versine = get_val(('Measured', 'Versine'))
                se = get_val(('Measured', 'Super Elevation'))
                gauge = get_val(('Measured', 'Gauge'))
                lateral = get_val(('Wear', 'Lateral'))
                vertical = get_val(('Wear', 'Vertical'))
                total_loss = get_val(('Wear', 'Total Loss of Section'))
            else:
                print(f"  -> Not in Excel. Filling with '0'.")
                versine = "0"
                se = "0"
                gauge = "0"
                lateral = "0"
                vertical = "0"
                total_loss = "0"

            try:
                def fill_field(name, value):
                    # Check if field exists on page before filling?
                    # Playwright locator.fill() will throw if element not attached/visible
                    # But if the column is missing in the FORM, the input might not exist.
                    # We can try/except individual fills.
                    try:
                        loc = target_page.locator(f'input[name="{name}"]').nth(i)
                        if loc.count() > 0:
                            loc.fill(value)
                    except Exception as fill_err:
                        # Ignore if field is missing on form
                        pass
                
                fill_field("versine", versine)
                fill_field("se", se)
                fill_field("gauge", gauge)
                fill_field("lateral", lateral)
                fill_field("vertical", vertical)
                fill_field("sectionloss", total_loss)
                
            except Exception as e:
                print(f"  Error filling station {station_str}: {e}")

        print("Data entry complete!")

if __name__ == "__main__":
    run()
