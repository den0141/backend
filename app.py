from fastapi import FastAPI, Request
import httpx

app = FastAPI()

API_BASE = "https://oldprison-prod.luckygem.online/api/player/init"

@app.post("/get_profile")
async def get_profile(req: Request):
    data = await req.json()
    tg_data = data.get("tgData")
    if not tg_data:
        return {"success": False, "error": "Нет данных Telegram"}

    # Из tg_data нужно извлечь query_id
    import urllib.parse, json
    parsed = urllib.parse.parse_qs(urllib.parse.unquote(tg_data.split("#tgWebAppData=")[-1]))
    query_id = parsed.get("query_id", [None])[0]
    if not query_id:
        return {"success": False, "error": "Нет query_id"}

    # Отправляем запрос в игру
    try:
        headers = {"Authorization": f"Bearer {query_id}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(API_BASE, headers=headers)
            profile = resp.json()
        return profile
    except Exception as e:
        return {"success": False, "error": str(e)}
