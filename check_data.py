import sqlite3

def check_stn(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM a_prl")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT STN) FROM a_prl")
    distinct = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM a_prl WHERE STN IS NULL")
    nulls = cursor.fetchone()[0]
    
    print(f"Total rows: {total}")
    print(f"Distinct STN: {distinct}")
    print(f"Null STN: {nulls}")

if __name__ == "__main__":
    check_stn(r'C:\Users\Athuv\.gemini\antigravity\scratch\track_profiling.db')
