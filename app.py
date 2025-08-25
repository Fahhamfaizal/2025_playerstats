import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from nl_to_sql import nl_to_sql

# --- Load API Key ---
load_dotenv()  # load from .env (local)
groq_api_key = os.getenv("GROQ_API_KEY")

# If running on Streamlit Cloud, use secrets.toml
if not groq_api_key and "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]

if not groq_api_key:
    st.error("❌ Groq API key not found. Please set it in `.env` (local) or `.streamlit/secrets.toml` (cloud).")
    st.stop()

# --- Groq Client ---
client = Groq(api_key=groq_api_key)

# --- Streamlit Config ---
st.set_page_config(page_title="⚽ Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")
st.sidebar.success("Using Groq API ✅")

# --- User Input ---
question = st.text_input("Ask me a football question in plain English:")

if question:
    # Convert NL -> SQL
    sql_query = nl_to_sql(question)
    st.write(f"**🔎 SQL Query:** `{sql_query}`")

    try:
        # Connect to database
        conn = sqlite3.connect("database/Top_500_players_2024.db")
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        if not df.empty:
            st.dataframe(df)

            # Plot if numeric data
            if df.select_dtypes(include=["int64", "float64"]).shape[1] > 0:
                st.write("📊 Visualization")
                df.plot(kind="bar", figsize=(8,4))
                st.pyplot(plt)

            # Summary with Groq
            summary_prompt = f"Summarize these football stats in simple words:\n{df.to_string()}"
            summary = client.chat.completions.create(
                messages=[{"role": "user", "content": summary_prompt}],
                model="mixtral-8x7b-32768"
            )
            st.write("📝 Summary:", summary.choices[0].message["content"])

        else:
            st.warning("No results found for your query.")

    except Exception as e:
        st.error(f"⚠️ SQL execution error: {e}")

