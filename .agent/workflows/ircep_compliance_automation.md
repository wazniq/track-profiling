---
description: Automate filling of compliance forms on IRCEP TMS website with randomized dates
---

This workflow automates the process of filling compliance forms for "Locations Needing Attention" on the IRCEP website.

1. **Prerequisites**:
   - The user must be logged into `https://ircep.gov.in/TMS/HomeIframe.jsp`.
   - The user must be on the "Location Needing Attention" page (Work -> Location Needing Attention).

2. **Automation Logic**:
   - The agent should use the `browser_subagent` to iterate through all items.
   - **Target**: `iframe[name="tmscontent"]` -> `img[id="comp"]` (Compliance buttons).
   - **Process**:
     - Count the total items.
     - Loop through each index.
     - Click the compliance button (using JS in the iframe).
     - Wait for the popup (`ExceptionCompPopUp.jsp`).
     - **Date Calculation**:
       - Read "Inspection Date" from the popup.
       - Add a random number of days between 30 and 45.
     - **Form Filling**:
       - `input[id="compworkdate"]`: Calculated Date (DD/MM/YYYY).
       - `textarea.form-control` (or second input): "attended".
     - **Submit**: Click the Submit button (`btn-success`).
     - Wait for the popup to close.

3. **Turbo Mode**:
   - Use `SafeToAutoRun: true` for all JavaScript executions to avoid user prompts for every item.
