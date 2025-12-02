import pandas as pd

file_path = 'Test.xlsx'
try:
    # Read with multi-index header (first 2 rows)
    df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])
    print("Columns:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
        
    print("\nFirst row of data:")
    print(df.iloc[0])
except Exception as e:
    print(f"Error: {e}")
