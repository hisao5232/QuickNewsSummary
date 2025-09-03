FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

WORKDIR /app

# 依存パッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps

# アプリ本体をコピー
COPY scraper.py .

# 直接 Python を起動
CMD ["python", "scraper.py"]
