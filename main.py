# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# =======================
#   CORS — разрешаем GitHub Pages
# =======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://den0141.github.io"],  # ссылка на твой WebApp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
#   Модель запроса
# =======================
class LoginRequest(BaseModel):
    initData: str

# =======================
#   Эндпоинт логина
# =======================
@app.post("/api/login")
async def login(req: LoginRequest):
    # Эмуляция запроса к игре (заменить на настоящий API игры)
    GAME_URL = "https://oldprison-prod.luckygem.online/api/auth/login"

    payload = {"initData": req.initData}

    try:
        game_response = requests.post(GAME_URL, json=payload, timeout=10)
        return game_response.json()
    except:
        return {"success": False, "detail": "Ошибка авторизации в игре"}

@app.get("/")
async def root():
    return {"status": "backend OK"}
