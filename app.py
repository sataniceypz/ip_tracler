from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Get credentials from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
IP_REGISTRY_API_KEY = os.getenv('IP_REGISTRY_API_KEY')

@app.route('/')
def log_ip():
    # Get the public IP address of the user
    user_ip = requests.get("https://api64.ipify.org?format=json").json().get('ip')

    # Call the ipregistry API with your API Key
    location_data = requests.get(f'https://api.ipregistry.co/{user_ip}?key={IP_REGISTRY_API_KEY}').json()

    # Extract available details
    ip_address = location_data.get('ip', 'Unknown IP')
    city = location_data.get('location', {}).get('city', 'Unknown City')
    region = location_data.get('location', {}).get('region', {}).get('name', 'Unknown Region')
    country = location_data.get('location', {}).get('country', {}).get('name', 'Unknown Country')
    isp = location_data.get('company', {}).get('name', 'Unknown ISP')

    # Additional information
    timezone = location_data.get('time_zone', {}).get('current_time', 'Unknown Time')
    latitude = location_data.get('location', {}).get('latitude', 'Unknown Latitude')
    longitude = location_data.get('location', {}).get('longitude', 'Unknown Longitude')
    postal = location_data.get('location', {}).get('postal', 'Unknown Postal Code')

    # Prepare the message
    location_info = (f"New Visitor:\n"
                     f"IP Address: {ip_address}\n"
                     f"City: {city}\n"
                     f"Region: {region}\n"
                     f"Country: {country}\n"
                     f"ISP: {isp}\n"
                     f"Latitude: {latitude}\n"
                     f"Longitude: {longitude}\n"
                     f"Postal Code: {postal}\n"
                     f"Timezone: {timezone}\n"
                     f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Send to Telegram
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data={
        'chat_id': TELEGRAM_CHAT_ID,
        'text': location_info
    })

    return "Thanks for visiting!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
