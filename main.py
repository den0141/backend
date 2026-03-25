from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# =======================
#   CORS
# =======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде лучше конкретный origin WebApp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
#   Модели запросов
# =======================
class LoginRequest(BaseModel):
    initData: str

class ResourceRequest(BaseModel):
    access_token: str

# =======================
#   Эндпоинт логина через initData
# =======================
@app.post("/api/login")
async def login(req: LoginRequest):
    GAME_URL = "https://oldprison-prod.luckygem.online/api/auth/login"
    payload = {"initData": req.initData}
    game_response = requests.post(GAME_URL, json=payload)
    try:
        return game_response.json()
    except:
        return {"error": True, "detail": "game response invalid"}

# =======================
#   Эндпоинт ресурсов игрока
# =======================
@app.post("/api/resources")
async def resources(req: ResourceRequest):
    # Подставляем реальный API игры
    GAME_RESOURCES_URL = "https://oldprison-prod.luckygem.online/api/player/init"

    headers = {"Authorization": f"Bearer {req.access_token}"}
    game_response = requests.post(GAME_RESOURCES_URL, headers=headers)

    try:
        data = game_response.json()
        currencies = data.get("currencies", {})
        return {
            "success": True,
            "rubles": currencies.get("rubles", 0),
            "cigarettes": currencies.get("cigarettes", 0),
            "sugar": currencies.get("sugar", 0)
        }
    except:
        return {"success": False, "detail": "Не удалось получить данные игрока"}

# =======================
#   Простейший корень
# =======================
@app.get("/")
async def root():
    return {"status": "backend OK"}
