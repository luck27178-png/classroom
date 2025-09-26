import streamlit as st
import pandas as pd
import os
import csv

# File to store persistent balances
DATA_FILE = "balances.csv"

# Initialize student balances
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, index_col=0)
    st.session_state.students = df['EduCoins'].to_dict()
else:
    st.session_state.students = {
        "Alice": 0,
        "Bob": 0,
        "Charlie": 0,
        "David": 0
    }

st.title("🎓 Classroom Cryptocurrency - EduCoin")
st.write("Earn, transfer, and track EduCoins in a gamified classroom!")

# --- Teacher Section ---
st.sidebar.header("Teacher Actions")
student_names = list(st.session_state.students.keys())
reward_student = st.sidebar.selectbox("Select student to reward:", student_names)
if st.sidebar.button("Give 1 EduCoin"):
    st.session_state.students[reward_student] += 1
    st.sidebar.success(f"1 EduCoin given to {reward_student}!")

# --- Student Section ---
st.sidebar.header("Student Actions")
sender = st.sidebar.selectbox("Sender", student_names)
receiver = st.sidebar.selectbox("Receiver", student_names)
transfer_amount = st.sidebar.number_input("Amount to transfer", min_value=1, step=1)

if st.sidebar.button("Transfer Coins"):
    if sender == receiver:
        st.sidebar.error("Sender and receiver cannot be the same!")
    elif st.session_state.students[sender] < transfer_amount:
        st.sidebar.error("Insufficient balance!")
    else:
        st.session_state.students[sender] -= transfer_amount
        st.session_state.students[receiver] += transfer_amount
        st.sidebar.success(f"{transfer_amount} EduCoin transferred from {sender} to {receiver}!")

# --- Display Balances ---
st.header("📊 Student Balances")
balances_df = pd.DataFrame.from_dict(st.session_state.students, orient='index', columns=['EduCoins'])
balances_df = balances_df.sort_values(by='EduCoins', ascending=False)
st.dataframe(balances_df)

# --- Leaderboard ---
st.header("🏆 Leaderboard")
for idx, (student, coins) in enumerate(balances_df.iterrows(), start=1):
    st.write(f"{idx}. {student} - {coins['EduCoins']} EduCoins")

# --- Save balances persistently ---
balances_df.to_csv(DATA_FILE)
