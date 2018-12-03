import os

from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler)

app = Flask(__name__)

user_list = {}

try:
    # 0 -> CHANNEL_ACCESS_TOKEN
    CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']

    # 1 -> CHANNEL_SERECT
    CHANNEL_SERECT = os.environ['CHANNEL_SERECT']
except IndexError as e:
    print('CHANNEL_ACCESS_TOKEN or CHANNEL_SERECT not given')
    raise e

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SERECT)