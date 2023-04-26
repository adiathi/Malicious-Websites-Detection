from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

import pickle
import joblib

# Load the label encoder object from the pickle file
with open('CharsetEncoder.pkl', 'rb') as f:
    CharsetEncoder = pickle.load(f)

with open('ServerEncoder.pkl', 'rb') as f:
    ServerEncoder = pickle.load(f)
    
model = joblib.load('MaliciousWebsiteDetectorModel.pkl')


def calculate_days_difference(start_date):
    try:      
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference between current date and start date
        days_difference = (current_date - start_date).days

        return days_difference
    
    except ValueError:
        print("Invalid date format. Please enter date in dd/mm/yyyy HH:MM format.")

# Route for the home page
@app.route('/')
def home():
    return render_template('main.html')

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    number_special_character = request.form['number_special_character']
    charset = request.form['charset']
    server = request.form['server']
    site_reg_date = request.form['site_reg_date']
    Charset_encoded_value = CharsetEncoder.transform([charset])
    server_encoded_value = ServerEncoder.transform([server])
    site_age= calculate_days_difference(site_reg_date)
    data = {
        "NUMBER_SPECIAL_CHARACTERS": [number_special_character],
        "CHARSET_TYPE": [charset],
        "SERVER_TYPE": [server_encoded_value],
        "SITE_AGE": [site_age]
    }

    df = pd.DataFrame(data)
    prediction = model.predict(df)
    

    # Prepare the response data
    response = {
        'prediction': prediction
    }

    # Return the response as JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
