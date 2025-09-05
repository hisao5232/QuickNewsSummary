# Node.js イメージを利用
FROM node:18-alpine

WORKDIR /app

# package.json をコピー
COPY package.json package-lock.json* ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY . .

# 開発サーバーを起動
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
