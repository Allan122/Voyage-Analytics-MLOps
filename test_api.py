import requests

# The URL of your local API
url = 'http://127.0.0.1:5000/predict_price'

# A fake flight booking a user might type into a website
fake_flight_data = {
    "distance_log": 6.5,          # Approximated logged distance
    "flight_month": 12,           # December
    "flight_day_of_week": 4,      # Friday
    "flightType_economic": 1,     # 1 means Yes (Economic class)
    "flightType_premium": 0,      # 0 means No
    "agency_CloudFy": 1           # Booked via CloudFy
}

print("Sending flight data to API...")
response = requests.post(url, json=fake_flight_data)

# Print the API's response
print("API Response:")
print(response.json())
