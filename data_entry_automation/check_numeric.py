import pandas as pd
import numpy as np

file_path = 'Test.xlsx'
try:
    df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])
    df = df[df[('Station', 'No.')].notna()]
    
    cols_to_check = [
        ('Measured', 'Versine'),
        ('Measured', 'Super Elevation'),
        ('Measured', 'Gauge'),
        ('Wear', 'Lateral'),
        ('Wear', 'Vertical'),
        ('Wear', 'Total Loss of Section')
    ]
    
    print("Checking for non-numeric values...")
    for col in cols_to_check:
        # Convert to numeric, coerce errors to NaN
        numeric_vals = pd.to_numeric(df[col], errors='coerce')
        non_numeric = df[numeric_vals.isna()]
        
        if not non_numeric.empty:
            print(f"Column {col} has {len(non_numeric)} non-numeric values:")
            print(non_numeric[col].tolist())
            print("At stations:", non_numeric[('Station', 'No.')].tolist())
        else:
            print(f"Column {col} is all numeric.")
            
except Exception as e:
    print(f"Error: {e}")
