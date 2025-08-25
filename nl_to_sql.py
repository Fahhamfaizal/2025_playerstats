import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

from nl_to_sql import nl_to_sql

st.set_page_config(page_title="Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

# ✅ Automatically find DB file
DB_FILENAME = "Top_500_players_2024.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_FILENAME)

if not os.path.exists(DB_PATH):
    st.error(f"❌ Database file '{DB_FILENAME}' not found in app directory.")
else:
    question = st.text_input("Ask me a football question in plain English:")

    if question:
        try:
            # Convert natural language → SQL
            sql_query = nl_to_sql(question)
            st.write("📝 Generated SQL:", sql_query)

            # Connect in read-only mode for safety
            conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
            df = pd.read_sql_query(sql_query, conn)
            conn.close()

            # Show results
            st.subheader("📊 Query Results")
            st.dataframe(df)

            # Optional plot if numeric
            if not df.empty and df.select_dtypes(include=["int", "float"]).shape[1] > 0:
                st.subheader("📈 Visualization")
                df.plot(kind="bar", figsize=(8,4))
                st.pyplot(plt)

        except Exception as e:
            st.error(f"⚠️ SQL execution error: {e}")
