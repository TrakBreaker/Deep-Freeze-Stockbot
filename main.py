import requests
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask

# ---------- CONFIG ----------
URL = "https://www.cdkeys.com/fortnite-deep-freeze-bundle-pc-cd-key"
WEBHOOK_URL = "https://discord.com/api/webhooks/1407723689331523625/iQZj4CkgeYdb6arWJkRV3fTo72yXriWiU4BCWuDTuytrB8d1aZgXqapUoRmHWufa8VGE"
CHECK_INTERVAL = 60 * 10  # every 10 minutes
# ----------------------------

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Fortnite Stock Bot is running on Render!"

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return "out of stock" not in soup.text.lower()

def send_discord_notification():
    data = {
        "content": f"🎉 The **Fortnite Deep Freeze Bundle** is back in stock! Grab it here: {URL}"
    }
    requests.post(WEBHOOK_URL, json=data)

def loop_check():
    while True:
        try:
            if check_stock():
                send_discord_notification()
                print("✅ Item in stock! Discord notified.")
                time.sleep(CHECK_INTERVAL * 6)  # Wait 1 hr before next notification
            else:
                print("❌ Still out of stock. Checking again...")
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(CHECK_INTERVAL)

# Run stock checker in background thread
threading.Thread(target=loop_check, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
