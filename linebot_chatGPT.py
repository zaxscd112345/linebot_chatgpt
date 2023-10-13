from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "11bff5aa3444243632834160f80fbc5a"
channel_access_token = "p8z6U4vCAsX4mgkpQZTz8M6F7HLgxUdcJTR+w6X7kQUYFodk5sPObunuhOc84M3KjpAgmnZ8zSuXiio71DG1k7EzFuqREzsmYKmMjCBeL1Z14ChAoLlGRY0mihRHWDyp8m3KvOlrXgxuFW0jViUN1wdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()
