import streamlit as st
import pandas as pd
import pickle

# ================================
# Feature Creation Function
# ================================
def create_features(input_data, team_win_rate, h2h, venue_stats, latest_form):
    bt = input_data['batting_team']
    bl = input_data['bowling_team']
    venue = input_data['venue']

    bt_wr = team_win_rate.get(bt, 0.5)
    bl_wr = team_win_rate.get(bl, 0.5)
    win_rate_diff = bt_wr - bl_wr

    h2h_win = h2h.get((bt, bl), 0.5)

    bt_v = venue_stats.get((venue, bt), 0.5)
    bl_v = venue_stats.get((venue, bl), 0.5)
    venue_diff = bt_v - bl_v

    bt_form = latest_form.get(bt, 0.5)
    bl_form = latest_form.get(bl, 0.5)
    form_diff = bt_form - bl_form

    toss_win = 1 if input_data['toss_winner'] == bt else 0

    return {
        'batting_team': bt,
        'bowling_team': bl,
        'venue': venue,
        'toss_decision': input_data['toss_decision'],
        'toss_win': toss_win,
        'win_rate_diff': win_rate_diff,
        'h2h_win_rate': h2h_win,
        'venue_win_rate': venue_diff,
        'form_diff': form_diff,
    }

# ================================
# Load Models & Data
# ================================
model_lr = pickle.load(open("logistic_model.pkl", "rb"))
model_xgb = pickle.load(open("xgb_model.pkl", "rb"))

team_win_rate = pickle.load(open("team_win_rate.pkl", "rb"))
h2h = pickle.load(open("h2h.pkl", "rb"))
venue_stats = pickle.load(open("venue_stats.pkl", "rb"))
latest_form = pickle.load(open("latest_form.pkl", "rb"))

teams = pickle.load(open("teams.pkl", "rb"))
venues = pickle.load(open("venues.pkl", "rb"))

# ================================
# UI Title
# ================================
st.title("🏏 Cricket Match Predictor")

# ================================
# Sidebar
# ================================
st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Select Prediction Type",
    ["Pre Match Prediction", "Live Match Prediction"]
)

# ================================
# PRE MATCH SECTION
# ================================
if option == "Pre Match Prediction":

    st.header("Pre Match Prediction")

    batting_team = st.selectbox("Batting Team", teams)
    bowling_team = st.selectbox("Bowling Team", teams)
    venue = st.selectbox("Venue", venues)

    toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
    toss_winner = st.selectbox("Toss Winner", teams)

    # ====================
    # Validation
    # ====================
    if batting_team == bowling_team:
        st.error("Batting and Bowling teams cannot be same")
        st.stop()

    if toss_winner not in [batting_team, bowling_team]:
        st.error("Toss winner must be one of the selected teams")
        st.stop()

    # ====================
    # Prediction
    # ====================
    if st.button("Predict Pre Match"):

        user_input = {
            'batting_team': batting_team,
            'bowling_team': bowling_team,
            'venue': venue,
            'toss_decision': toss_decision,
            'toss_winner': toss_winner
        }

        features = create_features(
            user_input,
            team_win_rate,
            h2h,
            venue_stats,
            latest_form
        )

        input_df = pd.DataFrame([features])

        prob = model_lr.predict_proba(input_df)[0][1]

        bat_prob = prob
        bowl_prob = 1 - prob

        # ====================
        # Output
        # ====================
        st.subheader("Win Probability")

        st.write(f"{batting_team} Win Chance: {round(bat_prob*100,2)}%")
        st.write(f"{bowling_team} Win Chance: {round(bowl_prob*100,2)}%")

        st.progress(int(bat_prob * 100))

        if bat_prob > bowl_prob:
            st.success(f"{batting_team} likely to win ({round(bat_prob*100,2)}%)")
        else:
            st.success(f"{bowling_team} likely to win ({round(bowl_prob*100,2)}%)")

        st.info("Prediction based on team performance, head-to-head stats, venue record, and recent form.")

        # ====================
        # Insights
        # ====================
        # st.subheader("Match Insights")

        # st.write(f"Win Rate Diff: {round(features['win_rate_diff'],2)}")
        # st.write(f"Head-to-Head: {round(features['h2h_win_rate'],2)}")
        # st.write(f"Form Diff: {round(features['form_diff'],2)}")
        # st.write(f"Venue Advantage: {round(features['venue_win_rate'],2)}")

# ================================
# LIVE MATCH (NEXT STEP)
# ================================
elif option == "Live Match Prediction":

    st.header("Live Match Prediction")

    batting_team = st.selectbox("Batting Team", teams)
    bowling_team = st.selectbox("Bowling Team", teams)

    runs_left = st.number_input("Runs Left", min_value=0)
    balls_left = st.number_input("Balls Left", min_value=1)
    wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10)

    current_score = st.number_input("Current Score", min_value=0)
    overs_completed = st.number_input("Overs Completed", min_value=0.0)

    phase = st.selectbox("Match Phase", ["Powerplay", "Middle", "Death"])

    # ====================
    # Validation
    # ====================
    if batting_team == bowling_team:
        st.error("Teams cannot be same")
        st.stop()

    if balls_left == 0 and runs_left > 0:
        st.error("Invalid match situation")
        st.stop()

    # ====================
    # Prediction
    # ====================
    if st.button("Predict Live Match"):

        # avoid division errors
        if overs_completed == 0:
            current_run_rate = 0
        else:
            current_run_rate = current_score / overs_completed

        required_run_rate = (runs_left * 6) / balls_left
        run_rate_ratio = current_run_rate / required_run_rate if required_run_rate != 0 else 0

        input_df = pd.DataFrame({
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'current_run_rate': [current_run_rate],
            'required_run_rate': [required_run_rate],
            'run_rate_ratio': [run_rate_ratio],
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'phase': [phase]
        })

        prob = model_xgb.predict_proba(input_df)[0][1]

        bat_prob = prob
        bowl_prob = 1 - prob

        st.subheader("Win Probability")

        st.write(f"{batting_team} Win Chance: {round(bat_prob*100,2)}%")
        st.write(f"{bowling_team} Win Chance: {round(bowl_prob*100,2)}%")

        st.progress(int(bat_prob * 100))

        if bat_prob > bowl_prob:
            st.success(f"{batting_team} likely to win ({round(bat_prob*100,2)}%)")
        else:
            st.success(f"{bowling_team} likely to win ({round(bowl_prob*100,2)}%)")

        # ====================
        # Insights
        # ====================
        st.subheader("Live Match Insights")

        st.write(f"Current Run Rate: {round(current_run_rate,2)}")
        st.write(f"Required Run Rate: {round(required_run_rate,2)}")
        st.write(f"Run Rate Ratio: {round(run_rate_ratio,2)}")