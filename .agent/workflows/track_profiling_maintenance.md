---
description: How to maintain, run, and package the Track Profiling application
---

# Track Profiling Application Maintenance Workflow

This workflow documents the steps to run, modify, and package the Track Profiling application.

## 1. Environment Setup

Ensure you have Python installed. The application relies on the following libraries:
- `tkinter` (usually built-in)
- `pandas`
- `matplotlib`
- `sqlalchemy`
- `openpyxl` (for Excel I/O)
- `pyinstaller` (for packaging)

To install dependencies:
```bash
pip install pandas matplotlib sqlalchemy openpyxl pyinstaller
```

## 2. Running the Application Locally

To run the application for development or testing:

1.  Open a terminal in the project directory: `C:\Users\Athuv\.gemini\antigravity\scratch`
2.  Run the main script:
    ```bash
    python main.py
    ```

## 3. Making Changes

The application logic is split across several files:
-   `main.py`: Entry point.
-   `ui.py`: User Interface, Plotting, and Interaction logic.
-   `models.py`: Database models (SQLAlchemy).
-   `track_profiling.db`: SQLite database file.

**Common Tasks:**
-   **UI Changes**: Edit `ui.py`.
-   **Calculation Logic**: Edit `run_calculations` method in `ui.py`.
-   **Database Schema**: Edit `models.py` (requires DB migration/reset if changed).

## 4. Packaging the Application

To create a standalone `.exe` file for Windows:

1.  **Build with PyInstaller**:
    Run the following command in the terminal:
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --name "Track Profiling" --hidden-import=sqlalchemy.sql.default_comparator --hidden-import=babel.numbers main.py
    ```
    *Note: We use `python -m PyInstaller` to ensure the correct module is invoked.*

2.  **Distribute**:
    -   The executable will be created in the `dist` folder.
    -   **CRITICAL**: You MUST copy the `track_profiling.db` file into the same folder as the `.exe` for it to work.
    ```bash
    copy track_profiling.db dist\
    ```

3.  **Run**:
    -   Navigate to `dist/` and double-click `Track Profiling.exe`.

## 5. Troubleshooting Packaging

-   If the app fails to launch, try running it from a terminal to see error messages:
    ```bash
    .\dist\"Track Profiling.exe"
    ```
-   If you see "Module not found" errors, add `--hidden-import=module_name` to the PyInstaller command.
