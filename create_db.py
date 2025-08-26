import sqlite3
import pandas as pd

def create_database():
    """
    Creates football.db from Top_500_Players_2024.csv
    and saves it with a table named 'players'.
    """
    try:
        # Load CSV
        df = pd.read_csv("Top_500_Players_2024.csv")
        print(f"✅ Loaded CSV with {len(df)} rows and {len(df.columns)} columns")

        # Create SQLite database
        conn = sqlite3.connect("football.db")
        df.to_sql("players", conn, if_exists="replace", index=False)
        conn.close()

        print("✅ Database 'football.db' created with table 'players'")
    except Exception as e:
        print(f"❌ Error while creating database: {e}")

# Run only when script is executed directly
if __name__ == "__main__":
    create_database()

