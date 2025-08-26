import sqlite3
import pandas as pd
import os

csv_file = "Top_500_Players_2024.csv"
db_file = "football.db"

def create_database():
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return

    df = pd.read_csv(csv_file)
    # normalize headers
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    con = sqlite3.connect(db_file)
    df.to_sql("players", con, if_exists="replace", index=False)
    con.close()
    print(f"✅ Database '{db_file}' ready with {len(df)} rows.")

if __name__ == "__main__":
    create_database()
