---
description: Automate data entry for Curve Inspection form from Excel
---

This workflow automates the process of filling the Curve Inspection web form using data from an Excel file.

## Prerequisites
1.  **Excel File**: Ensure your data is in `Test.xlsx` (or update the script) with the correct headers.
2.  **Google Chrome**: Must be running with remote debugging enabled.
    *   Command: `& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"`
3.  **Web Form**: You must be logged in and have the "Curve Inspection" form open in Chrome.

## Steps

1.  Navigate to the project directory.
    ```powershell
    cd C:\Users\Athuv\.gemini\antigravity\scratch\data_entry_automation
    ```

2.  Run the automation script.
    ```powershell
    python fill_curve_inspection.py
    ```

3.  **Verify**: Watch the form being filled. The script will:
    *   Round values up to the next whole number.
    *   Fill '0' for stations missing in the Excel file.
    *   Dismiss any alerts automatically.
