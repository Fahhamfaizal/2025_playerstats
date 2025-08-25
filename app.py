import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

from nl_to_sql import nl_to_sql

st.set_page_config(page_title="⚽ Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

# ✅ Path to DB (absolute path to avoid 'unable to open database file')
DB_PATH = os.path.join(os.path.dirname(__file__), "Top_500_players_2024.db")

def run_query(sql_query):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        cols = [description[0] for description in cursor.description]
        conn.close()
        return pd.DataFrame(rows, columns=cols)
    except Exception as e:
        st.error(f"⚠️ SQL execution error: {e}")
        return None

# User input
question = st.text_input("Ask me a football question in plain English:")

if question:
    sql_query = nl_to_sql(question)

    st.write("🔎 SQL Query:", sql_query)

    df = run_query(sql_query)

    if df is not None and not df.empty:
        st.dataframe(df)

        # Quick visualization if numeric data exists
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            st.subheader("📊 Quick Visualization")
            plt.figure(figsize=(8, 4))
            df[numeric_cols].plot(kind='bar', legend=True)
            st.pyplot(plt)
    else:
        st.warning("⚠️ No results found for this query.")
