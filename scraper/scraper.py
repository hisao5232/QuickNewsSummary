import os
import asyncio
import mysql.connector
from playwright.async_api import async_playwright
from datetime import datetime, timedelta, timezone

# DB 接続情報を環境変数から取得
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "newsdb")

async def main():
    # MySQL接続
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        use_unicode=True
    )
    cursor = conn.cursor()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://kabutan.jp")

        links1 = await page.locator("div#tp_market_right > ul > li > div > a").all()
        links2 = await page.locator("div#tp_market_right > ul > li > a").all()
        all_links = {}
        for link in links1 + links2:
            # JST タイムゾーン
            JST = timezone(timedelta(hours=9))
            scraped_at = datetime.now(JST)
            href = await link.get_attribute("href")
            title = await link.inner_text()
            if href:
                if href.startswith("/"):
                    href = "https://kabutan.jp" + href
                all_links[href] = title

        # 各記事にアクセスして本文取得、DBに保存
        for href, title in all_links.items():
            try:
                await page.goto(href)
                body_div = page.locator("div.body")
                await body_div.wait_for(timeout=5000)
                content = await body_div.inner_text()
            except Exception:
                content = "なし"

            cursor.execute(
                "INSERT INTO news (title, href, content, scraped_at) VALUES (%s, %s, %s, %s)",
                (title, href, content, scraped_at)
            )
            conn.commit()
            print(f"Saved: {title}")

        await browser.close()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())
