from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# مسیر داینامیک برای فایل db.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.json")

# بارگذاری پایگاه داده
with open(DB_PATH, "r", encoding="utf-8-sig") as f:
    database = json.load(f)

@app.post("/diagnose")
async def diagnose(request: Request):
    data = await request.json()
    question = data.get("question", "").strip()

    for entry in database:
        if any(word in question for word in entry["keywords"]):
            return {"text": entry["text"], "audio": entry["audio"]}
    
    return {"text": "متاسفم، نتونستم مشکل رو پیدا کنم.", "audio": ""}
