from fastapi import FastAPI
import mysql.connector
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "https://quicknews-api.go-pro-world.net",  # サブドメインからのアクセス
    "https://quicknews.go-pro-world.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "newsuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "newpass")
DB_NAME = os.environ.get("DB_NAME", "newsdb")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        use_unicode=True
    )

@app.get("/news")
def get_news(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # dict形式で返す
    cursor.execute("SELECT id, title, href, content, scraped_at FROM news ORDER BY scraped_at DESC LIMIT %s", (limit,))
    result = cursor.fetchall()
    conn.close()
    return result
