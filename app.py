import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import json
import requests
import openai

DEEPL_API = os.environ["DEEPL_API"]
OPENAI_KEY = os.environ["OPENAI_KEY"]
LINE_CHANNEL_ACCESS_TOKEN   = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)

openai.api_key = OPENAI_KEY

def return_chatbot_text(input_text):
    en_text = request_deepl(input_text, "JA", "EN")
    text = """You are a good friend bot with a kind heart.
Q: Many things happened today. Will you listen to me?
A: Of course I will! I'm always here for you, my friend.
Q:{}
A:""".format(en_text)
    answer = request_openai(text)
    ja_answer = request_deepl(answer, "EN", "JA")
    return ja_answer

def request_deepl(text, source_lang, target_lang):

    # パラメータの指定
    params = {
                'auth_key' : DEEPL_API,
                'text' : text,
                'source_lang' : source_lang,
                "target_lang": target_lang
            }
    # リクエストを投げる
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    result = request.json()["translations"][0]["text"]
    return result

def request_openai(text):
    start_sequence = "\nA:"
    restart_sequence = "\nQ: "

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt= text,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def handler(event, context):
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        messageText = line_event.message.text

        output_text = return_chatbot_text(messageText).strip()

        LINE_BOT_API.reply_message(line_event.reply_token, TextSendMessage(output_text))

    LINE_HANDLER.handle(body, signature)
    return 0
