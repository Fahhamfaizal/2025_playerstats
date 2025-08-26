import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql
import difflib

DB_PATH = "football.db"

def run_query(sql_query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return rows, columns
    except Exception as e:
        return [], [str(e)]
    finally:
        conn.close()

def find_closest_names(input_name, limit=3):
    """Find closest matching names from DB if no exact match is found."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM players")
    all_names = [row[0] for row in cur.fetchall()]
    conn.close()

    matches = difflib.get_close_matches(input_name, all_names, n=limit, cutoff=0.4)
    return matches

def app():
    st.title("⚽ Football Stats Explorer")
    st.write("Ask questions about players (e.g., 'How many goals did Erling Haaland score?')")

    question = st.text_input("Your Question:")

    if st.button("Ask") and question.strip():
        sql_query = nl_to_sql(question)
        st.code(sql_query, language="sql")

        rows, columns = run_query(sql_query)

        if rows:
            # ✅ Display table
            st.success("✅ Results found")
            st.dataframe([dict(zip(columns, row)) for row in rows])

            # ✅ Show graph if numeric
            numeric_cols = [c for c in columns if all(isinstance(r[i], (int, float)) for i, r in enumerate(rows) if r[i] is not None)]
            if numeric_cols:
                st.write("### 📊 Visualization")
                for col in numeric_cols:
                    values = [row[columns.index(col)] for row in rows]
                    labels = [row[0] for row in rows]  # assumes first col is name
                    plt.figure(figsize=(6, 4))
                    plt.bar(labels, values)
                    plt.xlabel("Players")
                    plt.ylabel(col)
                    plt.title(f"{col} comparison")
                    st.pyplot(plt)

            # ✅ Summary
            if "goals" in columns:
                total_goals = sum([row[columns.index("goals")] for row in rows if row[columns.index("goals")] is not None])
                st.info(f"📖 Summary: The selected players scored a total of **{total_goals} goals**.")

        else:
            st.error(f"❌ No data found for: {question}")

            # 🔎 Suggest close matches
            if "haaland" in question.lower():
                st.warning("🔍 Checking for close matches...")
                matches = find_closest_names("Erling Haaland")
                if matches:
                    st.write("Did you mean:")
                    for m in matches:
                        st.write(f"- {m}")

if __name__ == "__main__":
    app()
