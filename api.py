import requests

TELEGRAM_BOT_TOKEN = "7659443094:AAHSU2xfqNTnSbaHWrZZTb_8RE7Rd5LdSOY"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code == 200:
        print("Сообщение отправлено!")
    else:
        print(f"Ошибка: {response.text}")

# Пример отправки сообщения
send_message("123456789", "Привет! Это тестовое сообщение.")
