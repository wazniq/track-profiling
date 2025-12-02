import os
import sqlite3
import pandas as pd
from dbfread import DBF
from sqlalchemy import create_engine

def migrate_dbf_to_sqlite(source_dir, db_path):
    # Create SQLite engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # List of DBF files to migrate
    # Based on file listing: CLST.DBF, FIELDREF.DBF, PRL.DBF, REF.DBF, RGST.DBF, RL.DBF, TRSUM.DBF, FOXUSER.DBF
    # We might skip FOXUSER as it's likely system data
    dbf_files = [f for f in os.listdir(source_dir) if f.upper().endswith('.DBF') and 'FOXUSER' not in f.upper()]
    
    print(f"Found {len(dbf_files)} DBF files to migrate.")
    
    for dbf_file in dbf_files:
        table_name = os.path.splitext(dbf_file)[0].lower()
        full_path = os.path.join(source_dir, dbf_file)
        
        print(f"Migrating {dbf_file} to table '{table_name}'...")
        
        try:
            # Read DBF file
            table = DBF(full_path, load=True, ignore_missing_memofile=True, char_decode_errors='ignore')
            
            # Convert to DataFrame
            df = pd.DataFrame(iter(table))
            
            # If DataFrame is empty, try to create it from field names
            if df.empty and table.field_names:
                df = pd.DataFrame(columns=table.field_names)

            
            # Sanitize column names
            df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df.columns]
            
            print(f"    Columns: {list(df.columns)}")
            
            # Write to SQLite
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            print(f"  - Imported {len(df)} records.")
            
        except Exception as e:
            print(f"  - Failed to import {dbf_file}: {e}")
            import traceback
            traceback.print_exc()

    # Check if .PRL files are actually DBFs
    prl_files = [f for f in os.listdir(source_dir) if f.upper().endswith('.PRL')]
    for prl_file in prl_files:
        print(f"Checking if {prl_file} is a DBF...")
        try:
            full_path = os.path.join(source_dir, prl_file)
            table = DBF(full_path, load=True, ignore_missing_memofile=True, char_decode_errors='ignore')
            print(f"  - YES! {prl_file} is a DBF with {len(table)} records.")
            
            # Import it
            df = pd.DataFrame(iter(table))
            if df.empty and table.field_names:
                df = pd.DataFrame(columns=table.field_names)
            
            df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df.columns]
            
            # Add ID column for Primary Key
            df['id'] = range(1, len(df) + 1)
            
            table_name = os.path.splitext(prl_file)[0].lower() + "_prl"
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"  - Imported to table '{table_name}'")
            
        except:
            print(f"  - No, {prl_file} is likely binary or custom format.")

    # Check if .RL files are actually DBFs
    rl_files = [f for f in os.listdir(source_dir) if f.upper().endswith('.RL')]
    for rl_file in rl_files:
        print(f"Checking if {rl_file} is a DBF...")
        try:
            full_path = os.path.join(source_dir, rl_file)
            table = DBF(full_path, load=True, ignore_missing_memofile=True, char_decode_errors='ignore')
            print(f"  - YES! {rl_file} is a DBF with {len(table)} records.")
            
            # Import it
            df = pd.DataFrame(iter(table))
            if df.empty and table.field_names:
                df = pd.DataFrame(columns=table.field_names)
            
            df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df.columns]
            
            # Add ID column for Primary Key
            df['id'] = range(1, len(df) + 1)
            
            table_name = os.path.splitext(rl_file)[0].lower() + "_rl"
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"  - Imported to table '{table_name}'")
            print(f"  - Columns: {list(df.columns)}")
            
        except:
            print(f"  - No, {rl_file} is likely binary or custom format.")

    print("\nMigration completed.")

if __name__ == "__main__":
    SOURCE_DIR = r'C:\Users\Athuv\.gemini\antigravity\scratch\legacy_app\TS'
    DB_PATH = r'C:\Users\Athuv\.gemini\antigravity\scratch\track_profiling.db'
    
    migrate_dbf_to_sqlite(SOURCE_DIR, DB_PATH)
