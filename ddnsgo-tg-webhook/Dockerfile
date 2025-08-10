# 使用一個輕量的 Python 官方映像檔
FROM python:alpine3.22

# 設定工作目錄
WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式程式碼
COPY app.py .

# 開放容器的 8000 連接埠
EXPOSE 8000

# 設定環境變數 (僅為預設值，執行時應覆寫)
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# 執行 Gunicorn 伺服器
# -w 2: 啟動 2 個工作進程
# -b 0.0.0.0:8000: 監聽所有 IP 的 8000 連接埠
# app:app: 執行 app.py 中的 app 物件
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
