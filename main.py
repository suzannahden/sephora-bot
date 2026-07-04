import requests
from bs4 import BeautifulSoup
import os
import json
import time

URL = "https://gameon.sephora.pl/nagrody/katalog"

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_rewards():
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    rewards = []

    for h in soup.find_all(["h2", "h3", "h4"]):
        text = h.get_text(strip=True)
        if len(text) > 3:
            rewards.append(text)

    return list(set(rewards))

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

def main():
    if os.path.exists("rewards.json"):
        with open("rewards.json", "r", encoding="utf-8") as f:
            old = json.load(f)
    else:
        old = []

    current = get_rewards()

    new_rewards = [r for r in current if r not in old]

    if new_rewards:
        message = "🎁 Nowe nagrody Sephora:\\n\\n" + "\\n".join(new_rewards)
        send_telegram(message)

    with open("rewards.json", "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            send_telegram(f"Błąd bota: {e}")

        time.sleep(60)
