---
description: How to publish the Track Profiling application to GitHub
---

# Publishing to GitHub

Follow these steps to publish your **Track Profiling** application to GitHub.

## 1. Create a Repository on GitHub
1.  Log in to your [GitHub account](https://github.com/).
2.  Click the **+** icon in the top-right corner and select **New repository**.
3.  **Repository name**: Enter `track-profiling` (or your preferred name).
4.  **Description**: (Optional) "A desktop application for railway track profiling."
5.  **Public/Private**: Choose **Public** (since you want to open source it).
6.  **Initialize this repository with**: Leave all these unchecked (we already created README, .gitignore, and LICENSE locally).
7.  Click **Create repository**.

## 2. Push Your Code
Open your terminal in the project folder (`C:\Users\Athuv\.gemini\antigravity\scratch`) and run the following commands one by one:

### Step 2.1: Initialize Git
```bash
git init
```
*This sets up a new git repository in your folder.*

### Step 2.2: Add Files
```bash
git add .
```
*This stages all your files (code, documentation, images) for the first commit.*

### Step 2.3: Commit
```bash
git commit -m "Initial commit: Track Profiling App v1.0"
```
*This saves your changes locally.*

### Step 2.4: Rename Branch
```bash
git branch -M main
```
*This ensures your main branch is named 'main'.*

### Step 2.5: Link to GitHub
**Replace `YOUR_USERNAME` with your actual GitHub username:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/track-profiling.git
```
*This connects your local folder to the repository you created on GitHub.*

### Step 2.6: Push
```bash
git push -u origin main
```
*This uploads your code to GitHub. You may be asked to sign in.*

## 3. Verify
Refresh your GitHub repository page. You should see all your files, the README, and the License!
