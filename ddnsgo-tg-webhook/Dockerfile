# 1. 使用一個輕量的 Python 官方映像檔
FROM python:3.12-alpine3.24

# 2. 强制更新已安装的所有 apk 包到最新安全版本，并从 edge 升级 musl 以修复 CVE-2026-107891
RUN apk update && apk upgrade --no-cache && \
    apk upgrade --no-cache -X https://dl-cdn.alpinelinux.org/alpine/edge/main musl musl-utils

# 3. 随后再安装你的业务代码
WORKDIR /app

# 4. 複製依賴文件
COPY requirements.txt .

# 5. 安裝依賴并在构建完成后卸载 pip 及 ensurepip，彻底清除 pip/_vendor 内置旧依赖漏洞
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y pip && \
    rm -rf /usr/local/lib/python*/ensurepip /usr/local/bin/pip*

# 6. 複製應用程式程式碼
COPY app.py .

# 8.開放容器的 6789 連接埠
EXPOSE 6789

# 9.設定環境變數 (僅為預設值，執行時應覆寫)
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# 10.執行 Gunicorn 伺服器
# -w 2: 啟動 2 個工作進程
# -b 0.0.0.0:6789: 監聽所有 IP 的 6789 連接埠
# app:app: 執行 app.py 中的 app 物件
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:6789", "app:app"]
