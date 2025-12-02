# Track Profiling

A desktop application for managing and smoothing railway track profiles.

## Features

-   **Import Data**: Load Station and Existing Rail Levels (ERL) from Excel.
-   **Profile Management**: View and edit Station, ERL, and Proposed Rail Levels (PRL).
-   **Visualization**: Interactive plot showing ERL (Blue) and PRL (Red) profiles.
-   **Calculation**: Automatically calculate smoothed profiles based on Max Lift and Max Lower constraints.
-   **Validation**: Highlight rows that exceed defined lift/lower limits.
-   **Distribution Report**: Generate interpolated lift values for sub-stations (sleepers) between main stations.
-   **Export**: Export full results and reports to Excel.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/track-profiling.git
    cd track-profiling
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```

2.  **New Project**: File > New Project.
3.  **Import**: File > Import Excel... (or copy/paste data).
4.  **Calculate**: Click "Calculate" in the toolbar.
5.  **Export**: File > Export Excel...

## Building Executable

To build a standalone Windows executable:

```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "Track Profiling" --hidden-import=sqlalchemy.sql.default_comparator --hidden-import=babel.numbers main.py
```

The executable will be in the `dist/` folder. **Note:** You must keep `track_profiling.db` in the same folder as the executable.

## License

[MIT License](LICENSE)
