# Launch Chrome in Remote Debugging Mode
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$userDataDir = "C:\ChromeDebug"

Write-Host "Launching Chrome with Remote Debugging enabled..."
& $chromePath --remote-debugging-port=9222 --user-data-dir=$userDataDir

Write-Host "Chrome launched. Please log in and navigate to the Curve Inspection form."
