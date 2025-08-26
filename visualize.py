import os
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from create_db import create_database

# --- Ensure database exists ---
if not os.path.exists("football.db"):
    st.warning("⚠️ football.db not found, creating it...")
    create_database()

# --- Connect to DB ---
conn = sqlite3.connect("football.db")

st.title("📊 Football Player Stats Visualizer")

# User input
player_name = st.text_input("Enter a player's name (e.g., Lionel Messi):")

if player_name:
    try:
        query = "SELECT * FROM players WHERE Name = ?"
        df = pd.read_sql_query(query, conn, params=(player_name,))
        
        if not df.empty:
            st.success(f"✅ Found stats for {player_name}")
            st.dataframe(df)

            # --- Visualization ---
            numeric_cols = ["Goals", "Assists", "Yellow Cards", "Red Cards", "Own Goals"]
            player_stats = df[numeric_cols].iloc[0]

            fig, ax = plt.subplots()
            player_stats.plot(kind="bar", ax=ax)
            ax.set_title(f"{player_name} - Key Stats")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            
            st.pyplot(fig)

        else:
            st.error(f"❌ No data found for {player_name}")
    except Exception as e:
        st.error(f"⚠️ SQL error: {e}")
