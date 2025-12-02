import pandas as pd

file_path = 'Test.xlsx'
try:
    df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])
    # Filter valid stations
    df = df[df[('Station', 'No.')].notna()]
    
    # Check mandatory columns
    mandatory_cols = [
        ('Wear', 'Lateral'),
        ('Wear', 'Vertical'),
        ('Wear', 'Total Loss of Section')
    ]
    
    print("Checking for missing values in mandatory columns...")
    for col in mandatory_cols:
        missing = df[df[col].isna()]
        if not missing.empty:
            print(f"Column {col} has {len(missing)} missing values at stations:")
            print(missing[('Station', 'No.')].tolist())
        else:
            print(f"Column {col} is clean.")
            
except Exception as e:
    print(f"Error: {e}")
