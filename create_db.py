import sqlite3
import pandas as pd
import os

csv_file = "Top_500_Players_2024.csv"  # ✅ correct file name

# Step 1: Check if CSV exists
if not os.path.exists(csv_file):
    print(f"❌ CSV file not found: {csv_file}")
    exit()
else:
    print(f"✅ Found file: {csv_file}")

# Step 2: Load CSV
df = pd.read_csv(csv_file)
print(f"✅ Loaded CSV with {len(df)} rows and {len(df.columns)} columns")

# Step 3: Create / connect to SQLite DB
db_file = "football.db"
conn = sqlite3.connect(db_file)

# Step 4: Save to SQL table
df.to_sql("players", conn, if_exists="replace", index=False)

conn.close()
print(f"✅ Database '{db_file}' created with table 'players' ({len(df)} rows)")
