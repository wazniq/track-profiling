import sqlite3

def inspect_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # print("Tables:", tables)
    
    for table in tables:
        table_name = table[0]
        if 'a_prl' not in table_name: continue
        print(f"\nSchema for {table_name}:")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
        # Show first row
        print("  First row:")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        row = cursor.fetchone()
        print(f"  {row}")

if __name__ == "__main__":
    inspect_schema(r'C:\Users\Athuv\.gemini\antigravity\scratch\track_profiling.db')
