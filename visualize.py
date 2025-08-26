import streamlit as st
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql

st.set_page_config(page_title="Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

st.sidebar.success("Using AI Provider: Groq (Mixtral-8x7b)")

q = st.text_input("Ask me a football question:")

if q:
    try:
        sql = nl_to_sql(q)
        st.code(sql, language="sql")

        con = sqlite3.connect("football.db")
        df = pd.read_sql_query(sql, con)
        con.close()

        if not df.empty:
            st.subheader("📋 Query Results")
            st.dataframe(df)

            if df.shape == (1, 1):
                st.write(f"Answer: **{df.iloc[0,0]}**")
            else:
                st.write(f"Returned {df.shape[0]} rows and {df.shape[1]} columns.")

            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0:
                col = num_cols[0]
                st.subheader(f"📊 Visualization of {col}")

                if "name" in df.columns:
                    df_sorted = df.sort_values(col, ascending=False).head(10)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(df_sorted["name"], df_sorted[col], color="skyblue", edgecolor="black")
                    ax.set_title(f"Top 10 Players by {col.capitalize()}")
                    ax.set_ylabel(col.capitalize())
                    ax.set_xlabel("Player")
                    plt.xticks(rotation=45, ha="right")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.bar(df.index.astype(str), df[col], color="skyblue", edgecolor="black")
                    ax.set_title(f"{col} Values")
                    ax.set_ylabel(col.capitalize())
                    ax.set_xlabel("Index")
                    st.pyplot(fig)
                    plt.close(fig)
            else:
                st.info("⚠️ No numeric columns available for visualization.")

        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"SQL execution error: {e}")
