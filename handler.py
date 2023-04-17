import sys
sys.path.insert(0, 'vendor')

import os
import requests
import random
import json

PREFIX = '>'
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process_message(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }

def process_message(message):
    # Prevent self-reply
    if message['sender_type'] != 'bot':
        text = message['text']
        if text.startswith(PREFIX):
            return process_text(text.lstrip(PREFIX))

def process_text(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': text}],
        'max_tokens': 50,
        'temperature': 0.5,
        'stop': ['\n']
    }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return 'Error: ' + response.text.strip()


def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)
