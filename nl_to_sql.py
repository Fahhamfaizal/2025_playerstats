import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from nl_to_sql import nl_to_sql

st.set_page_config(page_title="⚽ Football Data Explorer", layout="wide")

# Title
st.title("⚽ Football Data Explorer")

# Input
question = st.text_input("Ask me a football question in plain English:")

if question:
    try:
        sql_query = nl_to_sql(question)

        # Connect DB
        conn = sqlite3.connect("Top_500_players_2024.db")
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        if df.empty:
            st.warning("No results found.")
        else:
            st.write("### Results", df)

            # Plot if numeric data exists
            numeric_cols = df.select_dtypes(include=["number"]).columns
            if len(numeric_cols) >= 1:
                col_to_plot = numeric_cols[0]
                st.write(f"### Visualization of `{col_to_plot}`")
                fig, ax = plt.subplots()
                df[col_to_plot].plot(kind="bar", ax=ax)
                st.pyplot(fig)

            # Summary
            st.write("### Summary")
            st.write(f"The query returned {len(df)} rows.")

    except Exception as e:
        st.error("⚠️ Error occurred while processing your request.")
        st.exception(e)
