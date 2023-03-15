#                                                                         Crypto Price Alert
Crypto Price Alert is a web application that allows users to monitor the prices of their favorite cryptocurrencies in real-time and receive alerts on WhatsApp when the prices break a specified threshold.

##Prerequisites
Before running the application, you will need to do the following:


Have a Twilio account and obtain an account SID and auth token.
Have a WhatsApp account and add Twilio's WhatsApp number to your contacts.

##Installation
Clone this repository to your local machine.
Create a virtual environment and activate it.
Install the required packages by running pip
Set the following environment variables:


TWILIO_ACCOUNT_SID: Your Twilio account SID.
TWILIO_AUTH_TOKEN: Your Twilio auth token.
TWILIO_PHONE_NUMBER: Your Twilio WhatsApp phone number.
YOUR_PHONE_NUMBER: Your WhatsApp phone number.
Run the application by running python app.py.


##Usage

Navigate to http://localhost:5000 in your web browser.
Enter the threshold prices for the cryptocurrencies you want to monitor.
Click the "Save" button to save the threshold prices.
Wait for the prices to update (which happens every 4 hours).
If a price breaks the threshold, you will receive a WhatsApp message from Twilio.


##How it works
The application uses the Binance API to fetch the current prices of the specified cryptocurrencies every 4 hours. If a price breaks the threshold, the application uses the Twilio API to send a WhatsApp message to the user's phone number. The user can update the threshold prices and delete cryptocurrencies from the list using the web interface.
