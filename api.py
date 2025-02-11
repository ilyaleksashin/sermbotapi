from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# ✅ ПРАВИЛЬНО: получаем токен из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не найден!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Определяем модель данных для запроса
class TelegramMessage(BaseModel):
    chat_id: str
    text: str

@app.get("/")
def home():
    """Главная страница API"""
    return {"message": "API работает!"}

@app.post("/telegram/message")
async def send_message_to_telegram(message: TelegramMessage):
    """Получает сообщение от Custom GPT и отправляет в Telegram"""
    payload = {
        "chat_id": message.chat_id,
        "text": message.text
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code == 200:
        return {"success": True, "message_id": response.json().get("result", {}).get("message_id")}
    else:
        raise HTTPException(status_code=400, detail=f"Ошибка отправки в Telegram: {response.text}")
