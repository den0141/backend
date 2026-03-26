from fastapi import FastAPI, Request
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем запросы с WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/player")
async def get_player(data: Request):
    body = await data.json()
    token = body.get("token")
    if not token:
        return {"error": "Токен не указан"}

    url = "https://oldprison-prod.luckygem.online/api/player/init"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "Ошибка получения профиля"}
    
    return resp.json()
