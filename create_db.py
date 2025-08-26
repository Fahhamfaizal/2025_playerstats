import pandas as pd
import sqlite3

# File paths
CSV_FILE = "Top_500_Players_2024.csv"
DB_FILE = "football.db"

def create_database():
    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # ✅ Normalize column names: lowercase + replace spaces with underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Save to SQLite
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("players", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    print(f"✅ Database '{DB_FILE}' created with table 'players' ({len(df)} rows).")

if __name__ == "__main__":
    create_database()
