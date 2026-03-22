from flask import Flask, render_template, request
import pickle
import pandas as pd
import urllib.parse

app = Flask(__name__)

# Load trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Feature extraction
def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_at'] = int('@' in url)
    features['has_dash'] = int('-' in url)
    features['https'] = int(url.startswith('https'))
    features['num_subdir'] = url.count('/')
    domain = urllib.parse.urlparse(url).netloc
    features['domain_length'] = len(domain)
    return pd.DataFrame([features])

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features = extract_features(url)
    prediction = model.predict(features)[0]
    result = "Phishing" if prediction == 1 else "Legitimate"
    return render_template('index.html', result=result, url=url)

if __name__ == '__main__':
    app.run(debug=True)