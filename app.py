from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ✅ あなたのLINEチャネルアクセストークンとシークレットを入れてね！
line_bot_api = LineBotApi('0YU5gWvZd3IlR/XO2S8L2U6LL/vPwQr6zV2pGoVFaYFOnhZcDx7WoxnAcR7G58j2TBj+FTYOTlI7bmDiQ39/8jhs4xDdnQSHqqmI9eG0RWE4Q7i/g8G/JdRFEPoxUYMXUq3nxrpRYdKxAyWPH+93lgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7f44df3f356e512ffb046676e56f46f0')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"エラー発生: {e}")
        return 'Error'
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    # 🔍 予約って言われたら特別な返事！
    if "予約" in msg or "よやく" in msg.lower():
        reply = "予約したい？🗓️ ご希望の日にちと時間を教えてね〜💖"
    else:
        reply = f'「{msg}」って言ったね💅なになに〜？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
