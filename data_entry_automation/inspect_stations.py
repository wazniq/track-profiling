import pandas as pd

file_path = 'Test.xlsx'
try:
    # Read with multi-index header (rows 0 and 1)
    df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])
    
    # The station column is likely the first one: ('Station', 'No.')
    # Let's print the first 10 station values
    print("First 10 Station values in Excel:")
    print(df.iloc[:10, 0].tolist())
    
    # Also print columns again to be super sure of indices
    print("\nColumns:")
    print(df.columns.tolist())
except Exception as e:
    print(f"Error: {e}")
