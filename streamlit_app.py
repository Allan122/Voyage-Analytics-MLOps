import streamlit as st
import joblib
import pandas as pd
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="Voyage Analytics", page_icon="✈️", layout="wide")
st.title("✈️ Voyage Analytics AI Platform")
st.write("Welcome to the next generation of travel intelligence. Use the AI to predict flight prices and discover personalized hotel stays.")

# --- 2. Load Models ---
@st.cache_resource # This caches the models so they don't reload every time you click a button
def load_models():
    reg = joblib.load('models/flight_price_regressor.joblib')
    scaler = joblib.load('models/data_scaler.joblib')
    knn = joblib.load('models/hotel_recommender.joblib')
    return reg, scaler, knn

try:
    regressor, data_scaler, recommender = load_models()
except Exception as e:
    st.error(f"Error loading models. Please ensure your .joblib files are in the 'models' folder. {e}")

# --- 3. Sidebar UI for User Inputs ---
st.sidebar.header("📝 Enter Trip Details")

# Flight Inputs
distance = st.sidebar.slider("Flight Distance (Miles)", min_value=100, max_value=5000, value=1000)
flight_class = st.sidebar.selectbox("Flight Class", ["Economic", "First Class"])
agency = st.sidebar.selectbox("Travel Agency", ["CloudFy", "Rainbow", "FlyingDrops"])

# Hotel Inputs (for Recommendation)
st.sidebar.markdown("---")
hotel_budget = st.sidebar.number_input("Hotel Budget (Total $)", min_value=50, max_value=5000, value=500)
days_staying = st.sidebar.slider("Days Staying", min_value=1, max_value=14, value=3)
user_age = st.sidebar.slider("Your Age", min_value=18, max_value=90, value=30)

# --- 4. Prediction Logic ---
if st.sidebar.button("🔮 Generate AI Predictions"):
    
    col1, col2 = st.columns(2)
    
    # --- FLIGHT PRICE PREDICTION ---
    with col1:
        st.subheader("🛫 Predicted Flight Ticket")
        
        # Format the input to match our scaler's expectations
        input_data = pd.DataFrame(0, index=[0], columns=data_scaler.feature_names_in_)
        
        # Apply the Log transformation we did in Colab
        input_data['distance_log'] = np.log1p(distance)
        
        # Map the dropdowns to One-Hot Encoding
        if flight_class == "Economic":
            if 'flightType_economic' in input_data.columns: input_data['flightType_economic'] = 1
        if agency == "CloudFy":
            if 'agency_CloudFy' in input_data.columns: input_data['agency_CloudFy'] = 1
        elif agency == "Rainbow":
            if 'agency_Rainbow' in input_data.columns: input_data['agency_Rainbow'] = 1
            
        # Scale and Predict
        scaled_features = data_scaler.transform(input_data)
        price_pred = regressor.predict(scaled_features)[0]
        
        st.success(f"### Estimated Price: ${price_pred:,.2f}")
        st.write(f"**Distance:** {distance} miles | **Class:** {flight_class} | **Agency:** {agency}")

    # --- HOTEL RECOMMENDATION ---
    with col2:
        st.subheader("🏨 Top Hotel Recommendations")
        
        # Create the profile array exactly as the KNN model expects it: [price, days, age]
        user_profile = [[hotel_budget, days_staying, user_age]]
        
        # Find the 5 closest matches
        distances, indices = recommender.kneighbors(user_profile)
        
        st.write("Based on your budget and travel profile, here are similar properties:")
        
        # Since we don't have the original hotel names dataframe loaded in the UI easily, 
        # we will display the mathematical similarity score to prove the engine works.
        for i in range(1, len(distances[0])):
            match_score = round((1 / (1 + distances[0][i])) * 100, 2) # Convert distance to a pseudo-accuracy percentage
            st.info(f"**Recommendation #{i}** — Profile Match Score: {match_score}%")
            
        st.caption("Note: In a full production environment, these indices would map directly to a live SQL database of hotel names and images.")
