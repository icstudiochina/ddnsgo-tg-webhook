# ddnsgo-tg-webhook
用於發送 Telegram Bot 通知的 ddns-go webhook 的 Docker 容器。  
A Docker container for ddns-go webhook used to send Telegram bot notifications.
  
### 部署步驟

1. 建立映像檔：  
在你的伺服器上，將 app.py, requirements.txt, Dockerfile 放在同一個目錄下 (ddns-telegram-webhook/)，然後執行以下指令：
```
cd ddns-telegram-webhook
docker build -t ddnsgo-tg-webhook .
```

2. 執行容器：  
使用 docker run 指令來啟動你的本地構建 Webhook 服務。記得將 YourBotToken 和 YourChatID 換成你自己的。
```
docker run -d \
 --name my-ddns-bot \
 -e TELEGRAM_BOT_TOKEN="<YourBotToken>" \
 -e TELEGRAM_CHAT_ID="<YourChatID>" \
 --restart always \
 ddnsgo-tg-webhook
```
或直接使用docker倉庫的鏡像：[icstudiocn/ddnsgo-tg-webhook](https://hub.docker.com/r/icstudiocn/ddnsgo-tg-webhook)
```
docker run -d \
 --name my-ddns-bot \
 -e TELEGRAM_BOT_TOKEN="<YourBotToken>" \
 -e TELEGRAM_CHAT_ID="<YourChatID>" \
 --restart always \
 icstudiocn/ddnsgo-tg-webhook
```

3. 設定 ddns-go：  
現在你的 Webhook 已經在 http://<你的伺服器IP>:6789/webhook 上運行了。最後一步就是設定 ddns-go。  
登入 ddns-go 的網頁管理介面。  
![ddns-go](https://github.com/icstudiochina/ddnsgo-tg-webhook/blob/master/ddnsgo-tg-webhook.jpg)
滑到底部的「Webhook」部分。在Webhook URL 填入你的服務地址，例如，http://<你的伺服器IP或域名>:6789/webhook  
強烈建議：為了安全，你應該使用 Nginx 或 Caddy 等反向代理，為你的 Webhook 配置一個域名和 HTTPS。這樣 URL 就會是 https://<你的伺服器IP或域名>/webhook。  
Webhook Request Body 填入你想要收到的訊息格式。   
一個推薦的格式如下（支援 Markdown）：
```
*DDNS 更新通知*
---------------------
IPv4域名: `#{ipv4Domains}`
IPv4狀態: `#{ipv4Result}`
最新 IPv4: `#{ipv4Addr}`
    
IPv6域名: `#{ipv6Domains}`
IPv6狀態: `#{ipv6Result}`
最新 IPv6: `#{ipv6Addr}`
```

4. DDNS-Go 更新通知：  
你可以手動觸發一次 ddns-go 的更新，來測試通知是否成功發送到你的 Telegram。
![tg-bot](https://github.com/icstudiochina/ddnsgo-tg-webhook/blob/master/tg-bot.jpg)

### 參考
模板變量參考：[https://github.com/jeessy2/ddns-go?tab=readme-ov-file#webhook](https://github.com/jeessy2/ddns-go?tab=readme-ov-file#webhook "https://github.com/jeessy2/ddns-go?tab=readme-ov-file#webhook")

| 变量名 | 说明 |
| ------------ | ------------ |
| #{ipv4Addr} | 新的IPv4地址 |
| #{ipv4Result} | IPv4地址更新结果: 未改变 失败 成功 |
| #{ipv4Domains} | IPv4的域名，多个以,分割 |
| #{ipv6Addr} | 新的IPv6地址 |
| #{ipv6Result} | IPv6地址更新结果: 未改变 失败 成功 |
| #{ipv6Domains} | IPv6的域名，多个以,分割 |
