import requests
import schedule
import time
from datetime import datetime

# Replace with your values
BOT_TOKEN = '8182530709:AAEeGHTNBCzr-OwTDbtFcrOqZ0xVAAZXoEk'
CHAT_ID = 1703188560  # keep as int, no quotes
NEWS_API_KEY = '08be9444be754314ba1cb70c225d1e82'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

def fetch_and_send_news():
    print(f"Fetching and sending news at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "SAP OR technology OR IB ACIO OR current affairs",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])[:3]

    if not articles:
        send_telegram_message("⚠️ No news found today.")
        return

    for article in articles:
        message = f"""📰 *{article['title']}*

{article.get('description', '')}

📅 {article['publishedAt'][:10]}
🔗 [Read more]({article['url']})
"""
        send_telegram_message(message)

# Schedule daily news sending at 7:30 AM
schedule.every().day.at("07:30").do(fetch_and_send_news)

# For testing now, call once immediately
fetch_and_send_news()

# Keep the script running and checking schedule
while True:
    schedule.run_pending()
    time.sleep(60)
