import telebot
import requests
import time

# আপনার সঠিক তথ্য
BOT_TOKEN = "8287589351:AAH_ENMT3Od1sQ2vttLUBgsIhaKuPBzC9ho" 
CHAT_ID = "-1003607510758" 
API_TOKEN = "f3-Ydn5PUTxHTg==" 

bot = telebot.TeleBot(BOT_TOKEN)

def check_and_send_otp():
    last_sent_otp = None
    print("বটটি এখন flysms.net প্যানেলে ওটিপি চেক করছে...")
    
    while True:
        try:
            # আপনার দেওয়া সঠিক প্যানেল ইউআরএল
            url = f"https://flysms.net/api/v2?action=getOrders&api_key={API_TOKEN}"
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                # যদি প্যানেলে কোনো অর্ডার থাকে
                if data and isinstance(data, list):
                    latest_order = data[0]
                    otp_code = latest_order.get('sms', 'No SMS yet')
                    
                    # নতুন ওটিপি আসলে গ্রুপে পাঠাবে
                    if otp_code != last_sent_otp and otp_code != 'No SMS yet':
                        message = f"📌 New OTP Received:\n\n💬 Code: {otp_code}\n👤 Owner: JAHANGIR"
                        bot.send_message(CHAT_ID, message)
                        last_sent_otp = otp_code
                        print(f"সফলভাবে ওটিপি পাঠানো হয়েছে: {otp_code}")
            else:
                print(f"প্যানেল এরর: {response.status_code}")
                
        except Exception as e:
            # লগে কোনো এরর আসলে এখানে দেখাবে
            print(f"কানেকশন সমস্যা: {e}")
        
        # প্রতি ১০ সেকেন্ড পর পর চেক করবে
        time.sleep(10)

if __name__ == "__main__":
    check_and_send_otp()
