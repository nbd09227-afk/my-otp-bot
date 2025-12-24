import telebot
import requests
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# আপনার তথ্য
BOT_TOKEN = "8287589351:AAH_ENMT3Od1sQ2vttLUBgsIhaKuPBzC9ho" 
CHAT_ID = "-1003607510758" 
API_TOKEN = "f3-Ydn5PUTxHTg==" 

bot = telebot.TeleBot(BOT_TOKEN)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

def check_and_send_otp():
    last_sent_otp = None
    print("বট সচল হয়েছে এবং ওটিপি চেক করছে...")
    while True:
        try:
            url = f"https://flysms.net/api/v2?action=getOrders&api_key={API_TOKEN}"
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    latest_order = data[0]
                    otp_code = latest_order.get('sms', 'No SMS yet')
                    
                    if otp_code != last_sent_otp and otp_code != 'No SMS yet':
                        message = f"📌 New OTP Received:\n\n💬 Code: {otp_code}\n👤 Owner: JAHANGIR"
                        bot.send_message(CHAT_ID, message)
                        last_sent_otp = otp_code
                        print(f"Group-এ ওটিপি পাঠানো হয়েছে: {otp_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    check_and_send_otp()
