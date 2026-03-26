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

class AuthRequest(BaseModel):
    token: str  # Bearer токен, который вводит пользователь


def get_player_data(token: str):
    url = "https://oldprison-prod.luckygem.online/api/player/init"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    response = requests.post(url, headers=headers)
    return response.json()


@app.post("/api/player")
async def load_player(data: AuthRequest):
    return get_player_data(data.token)
