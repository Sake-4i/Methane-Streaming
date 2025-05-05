import streamlit as st
import pandas as pd
import joblib

# Load model and scaler
try:
    model = joblib.load('methane_exceedance_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    st.error("Model or scaler not found. Please upload 'methane_exceedance_model.pkl' and 'scaler.pkl'.")
    st.stop()

st.title("Methane Exceedance Prediction Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file with readings:", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:", df.head())

    # Ensure the same column order used in training
    required_columns = ['AN422', 'BA1713_max', 'RH1712', 'TP1711', 'MM264', 'MM256']

    # Check if all required columns exist
    if all(col in df.columns for col in required_columns):
        try:
            X_input = df[required_columns].copy()
            X_scaled = scaler.transform(X_input)
            predictions = model.predict(X_scaled)

            df['Predicted_Exceed'] = predictions
            st.success("Prediction successful.")
            st.write(df[['Predicted_Exceed']].value_counts())
            st.dataframe(df[['Predicted_Exceed']].head())

            # Option to download results
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results", csv, "predictions.csv", "text/csv")

        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
    else:
        missing = list(set(required_columns) - set(df.columns))
        st.error(f"Missing required columns: {missing}")
