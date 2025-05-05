import streamlit as st
import pandas as pd
import joblib
import time
import os

st.title("Methane Monitoring Dashboard")
st.markdown("### Real-time Exceedance Alert System")

if os.path.exists("model.pkl") and os.path.exists("scaler.pkl"):
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
else:
    st.warning("Model or scaler not found. Please upload 'model.pkl' and 'scaler.pkl'.")
    st.stop()

if os.path.exists("dashboard_test_data.csv"):
    df = pd.read_csv("dashboard_test_data.csv")
else:
    st.warning("Test dataset not found. Please upload 'dashboard_test_data.csv'.")
    st.stop()

speed = st.slider("Speed (seconds between readings)", 0.1, 2.0, 1.0)
placeholder = st.empty()

for i in range(len(df)):
    row = df.iloc[[i]]
    features = row[['AN422', 'BA1713_max', 'RH1712', 'TP1711', 'MM264', 'MM256']]
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]

    with placeholder.container():
        st.write(f"### Reading {i+1}")
        st.dataframe(row)
        if prediction == 1:
            st.error("⚠️ Exceedance Detected!")
        else:
            st.success("✅ Normal")

    time.sleep(speed)
