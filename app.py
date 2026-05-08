from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

# Initialize the Flask App
app = Flask(__name__)

# Load the trained model and scaler at startup
# (Ensure your models folder has these exact file names)
try:
    regressor = joblib.load('models/flight_price_regressor.joblib')
    scaler = joblib.load('models/data_scaler.joblib')
    print("Model and Scaler loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Voyage Analytics Flight Price API is running!"})

@app.route('/predict_price', methods=['POST'])
def predict_price():
    try:
        # Get JSON data from the user's request
        data = request.get_json()
        
        # Convert JSON into a Pandas DataFrame
        input_df = pd.DataFrame([data])
        
        # We need to build a dataframe with the EXACT columns the scaler expects
        expected_cols = scaler.feature_names_in_
        
        # Create an empty dataframe with the exact columns, filled with 0
        final_df = pd.DataFrame(0, index=[0], columns=expected_cols)
        
        # Overwrite the 0s with the actual data the user provided
        for col in input_df.columns:
            if col in expected_cols:
                final_df[col] = input_df[col].values[0]
        
        # Scale the features
        input_scaled = scaler.transform(final_df)
        
        # Predict the price
        prediction = regressor.predict(input_scaled)[0]
        
        # Return the prediction as a JSON response
        return jsonify({
            "status": "success",
            "predicted_price_usd": round(prediction, 2)
        })

    except Exception as e:
        import traceback
        traceback.print_exc() # This will print the exact error to your terminal if it fails again
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    # Run the app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
