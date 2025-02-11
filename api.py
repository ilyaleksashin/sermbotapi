from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен Telegram-бота
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API-ключ Custom GPT
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Модель данных для сообщений
class TelegramMessage(BaseModel):
    chat_id: str
    text: str

@app.get("/")
def home():
    """Проверка работы API"""
    return {"message": "API работает!"}

@app.post("/telegram/message")
async def send_message_to_telegram(message: TelegramMessage):
    """Отправляет сообщение в Telegram"""
    payload = {"chat_id": message.chat_id, "text": message.text}
    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code == 200:
        return {"success": True, "message_id": response.json().get("result", {}).get("message_id")}
    else:
        raise HTTPException(status_code=400, detail=f"Ошибка Telegram API: {response.text}")

@app.post("/custom-gpt")
async def ask_custom_gpt(message: TelegramMessage):
    """Запрос в Custom GPT и отправка ответа в Telegram"""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": message.text}]
    }
    
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        gpt_response = response.json()["choices"][0]["message"]["content"]
        return await send_message_to_telegram(TelegramMessage(chat_id=message.chat_id, text=gpt_response))
    else:
        raise HTTPException(status_code=400, detail=f"Ошибка запроса в OpenAI: {response.text}")
