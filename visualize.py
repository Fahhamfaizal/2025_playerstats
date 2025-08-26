import sqlite3
import pandas as pd
import streamlit as st

# Connect to database
conn = sqlite3.connect("football.db")

# --- Simple NLP parser ---
def parse_question(question: str):
    """
    Parse natural language questions into (list of player_names, stat_col).
    Naive rule-based method.
    """
    stats_map = {
        "goals": "Goals",
        "assists": "Assists",
        "yellow cards": "Yellow Cards",
        "red cards": "Red Cards",
        "own goals": "Own Goals",
        "matches": "Matches Played",
        "age": "Age",
        "market value": "Market Value"
    }
    
    q_lower = question.lower()
    stat_col = None
    
    # detect which stat user is asking for
    for keyword, col in stats_map.items():
        if keyword in q_lower:
            stat_col = col
            break

    # crude name extraction
    player_names = []
    
    if " and " in q_lower:  # compare two players
        parts = q_lower.split(" and ")
        for part in parts:
            player_names.append(" ".join([w.capitalize() for w in part.split() if w.isalpha()]))
    elif " of " in q_lower:  # e.g. "goals of Lionel Messi"
        after_of = q_lower.split(" of ")[-1]
        player_names.append(" ".join([w.capitalize() for w in after_of.split() if w.isalpha()]))
    else:  # fallback: last 2 words
        words = question.split()
        player_names.append(" ".join(words[-2:]))
    
    return player_names, stat_col


# --- Streamlit UI ---
st.title("⚽ Football Stats Q&A")

question = st.text_input("Ask a football question (e.g., 'How many goals did Erling Haaland score?' or 'Compare goals of Messi and Ronaldo'):")

if question:
    player_names, stat_col = parse_question(question)

    if player_names and stat_col:
        results = {}
        for name in player_names:
            query = f"SELECT [{stat_col}] FROM players WHERE Name LIKE ?"
            df = pd.read_sql_query(query, conn, params=(f"%{name}%",))
            if not df.empty:
                results[name] = df.iloc[0,0]
            else:
                results[name] = None

        # Show results
        for name, value in results.items():
            if value is not None:
                st.success(f"✅ {name} has {value} {stat_col}")
            else:
                st.error(f"❌ No data found for {name}")

        # If multiple players → show bar chart + summary
        valid_results = {k:v for k,v in results.items() if v is not None}
        if len(valid_results) > 1:
            df_plot = pd.DataFrame.from_dict(valid_results, orient="index", columns=[stat_col])
            st.bar_chart(df_plot)

            # --- Summary sentence ---
            sorted_players = sorted(valid_results.items(), key=lambda x: x[1], reverse=True)
            top_player, top_value = sorted_players[0]
            second_player, second_value = sorted_players[1]
            if len(sorted_players) == 2:
                st.info(f"📊 Between {top_player} and {second_player}, {top_player} has more {stat_col} ({top_value} vs {second_value}).")
            else:
                st.info(f"📊 {top_player} leads all mentioned players with {top_value} {stat_col}.")
    else:
        st.error("⚠️ Could not understand the question. Try again.")
