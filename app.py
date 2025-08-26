import os
import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql
from groq import Groq

st.set_page_config(page_title="⚽ Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

DB_PATH = os.path.join(os.path.dirname(__file__), "football.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.sidebar.success("Using AI (Groq) for NL → SQL + Summaries")

question = st.text_input("Ask me a football question in plain English:")

if question:
    try:
        query = nl_to_sql(question)
        st.write("### 📝 Generated SQL")
        st.code(query, language="sql")

        df = pd.read_sql_query(query, conn)

        if not df.empty:
            st.write("### 📊 Query Results")
            st.dataframe(df, use_container_width=True)

            # --- Graph ---
            st.write("### 📈 Visualization")
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            if numeric_cols:
                col = numeric_cols[0]
                if "name" in df.columns:
                    fig, ax = plt.subplots(figsize=(6,4))
                    ax.barh(df["name"], df[col])
                    ax.set_xlabel(col.capitalize())
                    ax.set_ylabel("Player")
                    ax.set_title(f"{col.capitalize()} by Player")
                    ax.invert_yaxis()
                    st.pyplot(fig)
                else:
                    fig, ax = plt.subplots(figsize=(6,4))
                    df[col].plot(kind="hist", bins=10, ax=ax)
                    ax.set_xlabel(col.capitalize())
                    ax.set_title(f"Distribution of {col}")
                    st.pyplot(fig)
            else:
                st.info("No numeric columns available for graphing.")

            # --- AI Summary ---
            st.write("### 🤖 AI Summary")
            try:
                prompt = f"""
                Question: {question}
                Data (first 20 rows):
                {df.head(20).to_string(index=False)}
                Summarize in simple football terms.
                """
                res = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                )
                st.success(res.choices[0].message.content.strip())
            except Exception as e:
                st.warning(f"Could not generate summary: {e}")

        else:
            st.warning("No results found for your question.")
    except Exception as e:
        st.error(f"⚠️ SQL execution error: {e}")
else:
    st.info("Ask a question about 2024-25 season player stats")
