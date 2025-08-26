import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql

DB_FILE = "football.db"

# Run SQL query
def run_query(query: str):
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"⚠️ SQL execution error: {e}")
        df = pd.DataFrame()
    conn.close()
    return df

# Summarize results
def summarize(df: pd.DataFrame, question: str) -> str:
    if df.empty:
        return f"❌ No data found for '{question}'"

    # If single value
    if df.shape == (1, 1):
        col = df.columns[0]
        val = df.iloc[0, 0]
        return f"✅ Answer: {val} ({col})"

    return f"✅ Found {len(df)} rows matching your question."

# Visualization
def plot_data(df: pd.DataFrame):
    if df.empty:
        return

    st.subheader("📊 Visualization")
    try:
        if "goals" in df.columns and "name" in df.columns:
            top = df.sort_values("goals", ascending=False).head(10)
            fig, ax = plt.subplots()
            ax.bar(top["name"], top["goals"])
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)
        elif df.shape[1] == 2:  # any 2-column result
            fig, ax = plt.subplots()
            ax.bar(df.iloc[:, 0], df.iloc[:, 1])
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"⚠️ Could not plot data: {e}")

# Streamlit UI
def main():
    st.title("⚽ Football Data Explorer")

    question = st.text_input("Ask me a football question in plain English:")

    if st.button("Search") and question:
        sql_query = nl_to_sql(question)
        st.code(sql_query, language="sql")

        df = run_query(sql_query)
        st.dataframe(df)

        st.write(summarize(df, question))
        plot_data(df)

if __name__ == "__main__":
    main()
