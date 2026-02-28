import os
import requests
from flask import Flask, request, jsonify

# TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 為Docker Container部署時配置
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 檢查必要的環境變數是否已設定
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("請設定環境變數: TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

# --- 初始化 Flask 應用 ---
app = Flask(__name__)

# --- 定義 Webhook 路由 ---
# 為了安全，你可以將 'webhook' 換成一個更複雜、不易猜到的路徑
# 例如：@app.route('/webhook/aBcDeF12345', methods=['POST'])
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """
    接收來自 ddns-go 的請求並轉發到 Telegram。
    ddns-go 會將通知內容放在請求的 body 中。
    """
    # 直接獲取 POST 請求的原始 body 內容 (bytes)，並解碼為 utf-8 字串
    message_content = request.get_data(as_text=True)

    if not message_content:
        return jsonify({"status": "error", "message": "Request body is empty"}), 400

    # Telegram Bot API 的 URL
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # 準備要發送到 Telegram 的資料
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_content,
        'parse_mode': 'Markdown' # 你可以選擇性使用 Markdown 或 HTML 來格式化訊息
    }

    app.logger.info(f"正在發送訊息到 Telegram (Chat ID: {TELEGRAM_CHAT_ID})...")

    try:
        # 發送請求到 Telegram，添加 10 秒超時限制
        response = requests.post(telegram_api_url, json=payload, timeout=10)
        response.raise_for_status()  # 如果請求失敗 (例如 4xx 或 5xx)，會拋出異常

        app.logger.info(f"成功發送訊息到 Chat ID {TELEGRAM_CHAT_ID}")
        return jsonify({"status": "success", "message": "Notification sent to Telegram"}), 200

    except requests.exceptions.Timeout:
        app.logger.error("發送 Telegram 訊息超時！請檢查網路連通性或是否需要代理。")
        return jsonify({"status": "error", "message": "Timeout while sending to Telegram"}), 504
    except requests.exceptions.RequestException as e:
        app.logger.error(f"發送 Telegram 訊息失敗: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """一個簡單的健康檢查端點"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # 這個區塊僅用於本地開發測試，部署時應使用 gunicorn
    app.run(host='0.0.0.0', port=6789, debug=True)
