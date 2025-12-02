import sqlite3
import pandas as pd

def check_erl(db_path):
    conn = sqlite3.connect(db_path)
    
    # Check if ERL is populated in a_prl
    df = pd.read_sql_query("SELECT STN, ERL, PRL FROM a_prl LIMIT 20", conn)
    print("Sample data from a_prl:")
    print(df)
    
    # Check for non-zero ERL
    count = pd.read_sql_query("SELECT COUNT(*) FROM a_prl WHERE ERL != 0 AND ERL IS NOT NULL", conn).iloc[0,0]
    print(f"\nRecords with non-zero ERL: {count}")

if __name__ == "__main__":
    check_erl(r'C:\Users\Athuv\.gemini\antigravity\scratch\track_profiling.db')
