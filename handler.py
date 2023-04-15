import sys
sys.path.insert(0, 'vendor')

import os
import requests
import random
import json

PREFIX = '>'
OPENAI_ENDPOINT = 'https://api.gpt-3.5-turbo.com/query'
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

def process_text(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY
    }

    data = {
        'prompt': text,
        'max_tokens': 50,
        'temperature': 0.5,
        'stop': ['\n']
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()['choices'][0]['text']
    return 'Error: ' + response.text

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process_text(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def process(message):
    # Prevent self-reply
    if message['sender_type'] != 'bot':
        if message['text'].startswith(PREFIX):
            return random.choice(OPTIONS)


def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)
