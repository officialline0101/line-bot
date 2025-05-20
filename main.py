# main.py

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os

app = Flask(__name__)

# 💄環境変数からLINEのキーを読み取る
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    print("ギャル注意⚠️：LINEのトークン設定されてないよ！")
    exit(1)

handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"エラーだよ💦：{e}")
        abort(400)

    return "OK✨"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    reply_text = f"やっほ〜💌『{text}』って送ってくれたんだね❣️"
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=[
                {
                    "type": "text",
                    "text": reply_text
                }
            ]
        )

if __name__ == "__main__":
    app.run()
