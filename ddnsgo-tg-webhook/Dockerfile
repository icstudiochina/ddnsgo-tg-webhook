# 1. 使用一個輕量的 Python 官方映像檔
FROM python:3.12-alpine3.23
# FROM alpine:3.x

# 2.强制更新已安装的所有 apk 包到最新安全版本
RUN apk update && apk upgrade --no-cache

# 3. 修复 Pip 自身的漏洞
RUN pip install --no-cache-dir --upgrade pip

# 4. 随后再安装你的业务代码
WORKDIR /app

# 5.複製依賴文件
COPY requirements.txt .

# 6.安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 7.複製應用程式程式碼
COPY app.py .

# 8.開放容器的 8000 連接埠
EXPOSE 8000

# 9.設定環境變數 (僅為預設值，執行時應覆寫)
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# 10.執行 Gunicorn 伺服器
# -w 2: 啟動 2 個工作進程
# -b 0.0.0.0:8000: 監聽所有 IP 的 8000 連接埠
# app:app: 執行 app.py 中的 app 物件
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
