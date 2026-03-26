from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Модель входящих данных ===
class InitData(BaseModel):
    initData: str


# === ЗАГЛУШКА: здесь ты сам передаёшь данные игрока ===
# Позже сюда вставим запросы к игре.
mock_player_data = {
    "level": 16,
    "experience": 940,
    "nextLevelExperience": 17500,
    "energy": 202,
    "maxEnergy": 202,
    "currencies": {
        "Cash": 35976,
        "Gold": 48689,
        "PrisonCurrency": 155
    }
}


@app.post("/api/profile")
async def get_profile(data: InitData):
    # Тут ты можешь расшифровать initData
    # Или получить токен игрока

    return mock_player_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
