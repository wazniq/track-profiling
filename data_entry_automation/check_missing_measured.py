import pandas as pd

file_path = 'Test.xlsx'
try:
    df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])
    df = df[df[('Station', 'No.')].notna()]
    
    measured_cols = [
        ('Measured', 'Versine'),
        ('Measured', 'Super Elevation'),
        ('Measured', 'Gauge')
    ]
    
    print("Checking for missing values in Measured columns...")
    for col in measured_cols:
        missing = df[df[col].isna()]
        if not missing.empty:
            print(f"Column {col} has {len(missing)} missing values.")
            # print(missing[('Station', 'No.')].tolist())
        else:
            print(f"Column {col} is clean.")
            
except Exception as e:
    print(f"Error: {e}")
