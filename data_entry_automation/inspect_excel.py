import pandas as pd
import os

file_path = 'Test.xlsx'

try:
    # Try reading with openpyxl engine which is standard for xlsx
    df = pd.read_excel(file_path, engine='openpyxl', nrows=0)
    print("Headers found:")
    for col in df.columns:
        print(f"- {col}")
except Exception as e:
    print(f"Error reading Excel file: {e}")
