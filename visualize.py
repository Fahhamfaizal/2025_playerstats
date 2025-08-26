import streamlit as st
import sqlite3
import pandas as pd
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
            st.dataframe(df)

            if df.shape == (1, 1):
                st.write(f"Answer: **{df.iloc[0,0]}**")
            else:
                st.write(f"Returned {df.shape[0]} rows and {df.shape[1]} columns.")

            num_cols = df.select_dtypes(include=["int64", "float64"]).columns
            if len(num_cols) > 0:
                col = num_cols[0]   # pick first numeric col only
                plt.figure(figsize=(6,3))
                plt.bar(df.index, df[col])   # force single-column bar chart
                plt.xlabel("Index")
                plt.ylabel(col)
                st.pyplot(plt)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(e)
