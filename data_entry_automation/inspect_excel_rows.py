import pandas as pd

file_path = 'Test.xlsx'
try:
    # Read first 5 rows to see the header structure (likely multi-index)
    df = pd.read_excel(file_path, engine='openpyxl', header=None, nrows=5)
    print(df.to_string())
except Exception as e:
    print(f"Error: {e}")
