from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Разрешаем запросы с WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://den0141.github.io"],  # твой WebApp
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/player")
async def get_player(data: dict):
    token = data.get("token")
    if not token:
        return {"error": "Токен не предоставлен"}

    try:
        # Правильный URL: токен подставляется в путь
        url = f"https://oldprison-prod.luckygem.online/init/{token}"
        resp = requests.post(url, headers={"Content-Type": "application/json"})

        if resp.status_code != 200:
            return {"error": f"Не удалось получить профиль, статус {resp.status_code}"}

        profile = resp.json()
        # Проверка success
        if not profile.get("success", True):
            return {"error": "Токен неверный или просрочен"}

        return profile

    except Exception as e:
        return {"error": str(e)}
