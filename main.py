from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import urllib.parse
import json

app = FastAPI()

# Разрешаем доступ с WebApp GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно заменить на URL вашего WebApp
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthRequest(BaseModel):
    initData: str  # теперь принимаем полную строку

@app.post("/api/login")
async def login(req: AuthRequest):
    init_data = req.initData
    try:
        # Разбиваем параметры query_id, user, auth_date, signature
        params = urllib.parse.parse_qs(init_data)
        user_json = params.get("user")[0]  # берем значение user
        user_dict = json.loads(urllib.parse.unquote(user_json))  # декодируем JSON
        user_id = user_dict["id"]
        first_name = user_dict.get("first_name", "")
        print(f"Авторизация игрока: {first_name}, ID: {user_id}")
    except Exception as e:
        print("Ошибка разбора initData:", e)
        return {"success": False, "error": "Невалидный initData"}

    # TODO: здесь можно добавить проверку hash у Telegram
    return {"success": True}