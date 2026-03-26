from fastapi import FastAPI
import uvicorn
import requests
import urllib.parse

app = FastAPI()

GAME_INIT_URL = "https://oldprison-prod.luckygem.online/init/"
PLAYER_INIT_URL = "https://oldprison-prod.luckygem.online/api/player/init"


@app.post("/api/init")
def get_profile(data: dict):
    init_str = data.get("initData")

    if not init_str:
        return {"error": "Нет initData"}

    # 1. Декодируем URL
    decoded = urllib.parse.unquote(init_str)

    # 2. Извлекаем user JSON
    try:
        user_str = decoded.split("user=")[1].split("&")[0]
        user = urllib.parse.unquote(user_str)
        user_json = eval(user)
        player_id = user_json["id"]
    except:
        return {"error": "Ошибка парсинга initData"}

    # 3. Делаем запрос на получение игрового токена
    init_url = GAME_INIT_URL + init_str
    token_resp = requests.get(init_url)

    if token_resp.status_code != 200:
        return {"error": "Не удалось получить токен"}

    bearer = token_resp.json().get("accessToken")

    if not bearer:
        return {"error": "Токен не получен"}

    # 4. Теперь получаем профиль игрока
    headers = {"Authorization": f"Bearer {bearer}"}
    p = requests.post(PLAYER_INIT_URL, headers=headers)

    if p.status_code != 200:
        return {"error": "Ошибка получения профиля"}

    pdata = p.json()

    # 5. Возвращаем валюту
    return {
        "playerId": player_id,
        "money": pdata["player"].get("money", 0),
        "cigs": pdata["player"].get("cigarettes", 0),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
