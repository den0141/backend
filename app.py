from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://den0141.github.io"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/player")
async def get_player(data: dict):
    token = data.get("token")
    if not token:
        return {"error": "Токен не предоставлен"}

    url = "https://oldprison-prod.luckygem.online/api/player/init"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        resp = requests.post(url, headers=headers)
        if resp.status_code != 200:
            return {"error": f"Не удалось получить профиль, статус {resp.status_code}"}

        profile = resp.json()
        if not profile.get("success"):
            return {"error": "Токен неверный или просрочен"}

        return profile

    except Exception as e:
        return {"error": str(e)}
