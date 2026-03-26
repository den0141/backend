from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Разрешаем CORS для GitHub Pages
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
        return {"error": "No token provided"}

    # Запрос к реальному API игры
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post("https://oldprison-prod.luckygem.online/api/player/init", headers=headers)
    if resp.status_code != 200:
        return {"error": "Failed to fetch player data"}
    return resp.json()
