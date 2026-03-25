from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    initData: str

@app.post("/api/login")
async def login(req: LoginRequest):
    GAME_URL = "https://oldprison-prod.luckygem.online/api/auth/login"

    # ⚠️ Отправляем как form data
    payload = req.initData  # уже в формате query_id=...&user=...&auth_date=...&signature=...&hash=...
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    game_response = requests.post(GAME_URL, data=payload, headers=headers)

    try:
        return game_response.json()
    except:
        return {"error": True, "detail": "game response invalid"}
