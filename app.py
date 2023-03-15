import requests
import json
from twilio.rest import Client
from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Set the Twilio account details
account_sid = '*********************'
auth_token = '*********************'
twilio_phone_number = 'whatsapp:+*******'
your_phone_number = 'whatsapp:+***********'

# Set the API endpoint and query parameters for the 4-hour time frame
endpoint = 'https://api.binance.com/api/v3/klines'
interval = '4h'
limit = 1

# Set up the Twilio client
client = Client(account_sid, auth_token)

# Set the initial threshold prices and timestamp for each cryptocurrency token
crypto_tokens = {'FTM': {'threshold_price': 2.0, 'timestamp': None},
                 'XRP': {'threshold_price': 0.8, 'timestamp': None},
                 'ANC': {'threshold_price': 3.5, 'timestamp': None},
                 'DYDX': {'threshold_price': 10.0, 'timestamp': None},
                 'HNT': {'threshold_price': 10.0, 'timestamp': None}}

# Define the home page route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Update the threshold price for the given token name or delete the token
        token_name = request.form['token_name']
        if token_name in crypto_tokens:
            if 'delete' in request.form:
                del crypto_tokens[token_name]
            else:
                threshold_price = float(request.form['threshold_price'])
                crypto_tokens[token_name]['threshold_price'] = threshold_price
        else:
            threshold_price = float(request.form['threshold_price'])
            crypto_tokens[token_name] = {'threshold_price': threshold_price, 'timestamp': None}

    # Get the current prices and timestamps for each cryptocurrency token
    prices = {}
    for crypto_token in crypto_tokens:
        params = {'symbol': crypto_token + 'USDT', 'interval': interval, 'limit': limit}
        response = requests.get(endpoint, params=params)
        data = json.loads(response.text)
        price = float(data[0][4])
        prices[crypto_token] = price
        timestamp = datetime.fromtimestamp(data[0][0] / 1000) # Convert timestamp to datetime object
        crypto_tokens[crypto_token]['timestamp'] = timestamp

        # Check if the current time is a multiple of 4 hours from the start time
        if timestamp.hour % 4 == 0 and timestamp.minute == 0 and timestamp.second == 0:
            # Check if any of the threshold prices have been broken
            for crypto_token, data in crypto_tokens.items():
                threshold_price = data['threshold_price']
                timestamp = data['timestamp']
                if prices[crypto_token] > threshold_price:
                    # Send a message on WhatsApp using Twilio
                    message = f'Alert! {crypto_token} has broken {threshold_price} in the {interval} time frame at {timestamp}.'
                    client.messages.create(body=message, from_=twilio_phone_number, to=your_phone_number)

    return render_template('index.html', crypto_tokens=crypto_tokens, prices=prices)

if __name__ == '__main__':
    app.run(debug=True)
