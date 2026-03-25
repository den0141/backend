from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # временно для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    initData: str

@app.post("/api/login")
async def login(req: LoginRequest):
    GAME_URL = "https://oldprison-prod.luckygem.online/api/auth/login"
    payload = {"initData": req.initData}
    try:
        game_response = requests.post(GAME_URL, json=payload, timeout=10)
        return game_response.json()
    except:
        return {"success": False, "detail": "game response invalid"}

@app.get("/")
async def root():
    return {"status": "backend OK"}
