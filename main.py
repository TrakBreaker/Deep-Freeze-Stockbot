from flask import Flask
import requests
import time
import threading

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1407723689331523625/iQZj4CkgeYdb6arWJkRV3fTo72yXriWiU4BCWuDTuytrB8d1aZgXqapUoRmHWufa8VGE"

def check_stock():
    url = "https://store.epicgames.com/en-US/p/fortnite"  # placeholder, adjust if deep freeze has its own link
    while True:
        try:
            response = requests.get(url)
            if "Deep Freeze" in response.text:  # crude check
                requests.post(WEBHOOK_URL, json={"content": "🎉 Deep Freeze skin is in stock!"})
        except Exception as e:
            print("Error checking stock:", e)
        time.sleep(300)  # check every 5 mins

# Run stock checker in the background
threading.Thread(target=check_stock, daemon=True).start()

@app.route("/")
def home():
    return "Deep Freeze Stock Bot is running ✅"
