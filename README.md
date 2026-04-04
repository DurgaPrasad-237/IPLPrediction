# 🏏 IPL Match Prediction App

A machine learning-based web application that predicts IPL match outcomes using both **pre-match analysis** and **live match conditions**.

---

## 🚀 Overview

This project provides two types of predictions:

1. **Pre-Match Prediction** → Predicts winner before the match starts
2. **Live Match Prediction (2nd Innings)** → Predicts winning probability during the chase

The app is built using **Streamlit** and leverages multiple machine learning models trained on IPL historical data.

---

## 🧠 Models Used

### 🔹 Logistic Regression (Pre-Match Prediction)

Used to predict match outcome before the game starts.

### 🔹 XGBoost (Live Match Prediction)

Used to predict winning probability during the **second innings** based on live match conditions.

---

## 📊 Prediction Logic

### ✅ Pre-Match Prediction Inputs

* Batting Team
* Bowling Team
* Toss Winner
* Toss Decision (Bat / Field)
* Venue

👉 Output: **Predicted match winner**

---

### 🔥 Live Match Prediction (2nd Innings)

Predicts win probability during the chase using real-time match data:

* Batting Team
* Bowling Team
* Runs Left
* Balls Left
* Wickets Left
* Current Score
* Overs Completed
* Match Phase (Powerplay / Middle / Death)

👉 Output: **Winning probability (%)**

---

## 📂 Project Structure

```id="7cl9m2"
├── app.py
├── requirements.txt
├── logistic_model.pkl
├── xgb_model.pkl
├── teams.pkl
├── venues.pkl
├── venue_stats.pkl
├── team_win_rate.pkl
├── latest_form.pkl
├── h2h.pkl
```

---

## ⚙️ Features

* Dual prediction system (Pre-match + Live)
* Real-time win probability calculation
* Uses historical + contextual match data
* Interactive UI with Streamlit

---

## 🛠️ Installation

```id="qzt7he"
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py
```

---

## 📈 How It Works

### Pre-Match:

* Encodes categorical inputs (teams, venue, toss)
* Uses Logistic Regression to predict outcome

### Live Match:

* Calculates match state (runs left, balls left, etc.)
* Uses XGBoost to estimate winning probability dynamically

---

## ⚠️ Limitations

* Predictions are based only on historical data
* Does not include real-time factors like:

  * Player injuries
  * Weather conditions
  * Toss impact during live phase

---

## 🚀 Future Improvements

* Add player-level features
* Integrate live API data
* Improve model accuracy with feature engineering
* Add match visualization charts

---

## 💡 Author

Durga Prasad  
Aspiring Data Scientist | Machine Learning Enthusiast

---
