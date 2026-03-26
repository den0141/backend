from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Разрешаем GitHub Pages
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

    # Запрос к API игры
    try:
        resp = requests.post(
            f"https://oldprison-prod.luckygem.online/init/{token}",
            headers={"Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            return {"error": f"Failed to fetch profile, status {resp.status_code}"}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
