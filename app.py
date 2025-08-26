import os
import sqlite3
import streamlit as st
import pandas as pd
from create_db import create_database

# --- Ensure database exists ---
if not os.path.exists("football.db"):
    st.warning("⚠️ football.db not found, creating it...")
    create_database()

# --- Connect to DB ---
conn = sqlite3.connect("football.db")
cursor = conn.cursor()

st.title("⚽ Football Stats Explorer")

# User input
player_name = st.text_input("Enter a player's name (e.g., Erling Haaland):")

if player_name:
    try:
        query = "SELECT * FROM players WHERE Name = ?"
        df = pd.read_sql_query(query, conn, params=(player_name,))
        
        if not df.empty:
            st.success(f"✅ Found {len(df)} record(s) for {player_name}")
            st.dataframe(df)

            # Example: show Goals directly
            if "Goals" in df.columns:
                st.metric(label=f"Goals scored by {player_name}", value=int(df["Goals"].values[0]))

        else:
            st.error(f"❌ No data found for {player_name}")
    except Exception as e:
        st.error(f"⚠️ SQL error: {e}")
