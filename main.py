from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    game_response = requests.get(GAME_URL, params=payload)

    try:
        return game_response.json()
    except:
        return {"error": True, "detail": "game response invalid"}

@app.get("/")
async def root():
    return {"status": "backend OK"}
