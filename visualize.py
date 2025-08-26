import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql

st.set_page_config(page_title="Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

st.sidebar.success("Using AI Provider: Groq (Mixtral-8x7b)")

# User input
q = st.text_input("Ask me a football question:")

if q:
    try:
        # Convert natural language to SQL
        sql = nl_to_sql(q)
        st.code(sql, language="sql")

        # Run SQL query
        con = sqlite3.connect("football.db")
        df = pd.read_sql_query(sql, con)
        con.close()

        if not df.empty:
            st.subheader("📋 Query Results")
            st.dataframe(df)

            # If result is just one cell, show directly
            if df.shape == (1, 1):
                st.write(f"Answer: **{df.iloc[0,0]}**")
            else:
                st.write(f"Returned {df.shape[0]} rows and {df.shape[1]} columns.")

            # ==========================
            # Visualization Section
            # ==========================
            num_cols = df.select_dtypes(include=["number"]).columns
            if len(num_cols) > 0:
                col = num_cols[0]   # Pick first numeric column
                st.subheader("📊 Visualization")

                if "name" in df.columns:
                    # Show Top 10 for readability
                    df_sorted = df.sort_values(col, ascending=False).head(10)

                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(df_sorted["name"], df_sorted[col], color="skyblue", edgecolor="black")
                    ax.set_title(f"Top Players by {col.capitalize()}", fontsize=14, weight="bold")
                    ax.set_ylabel(col.capitalize())
                    ax.set_xticks(range(len(df_sorted["name"])))
                    ax.set_xticklabels(df_sorted["name"], rotation=45, ha="right")

                    st.pyplot(fig)   # ✅ Render chart
                else:
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.bar(df.index, df[col], color="skyblue", edgecolor="black")
                    ax.set_xlabel("Index")
                    ax.set_ylabel(col)
                    ax.set_title(f"Values of {col}")
                    st.pyplot(fig)
            else:
                st.info("No numeric columns available for visualization.")

        else:
            st.warning("No results found.")

    except Exception as e:
        st.error(f"SQL execution error: {e}")
