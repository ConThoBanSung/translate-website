import requests
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
import os

# Thay thế bằng API key hợp lệ từ Google Cloud Console
api_key = 'AIzaSyD1bCkgsZEZCaV3eJbb5Ec_ITAuDNOPG84'

# API endpoint của Gemini
api_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_language = request.form['language']
    translated_text = translate_text(text, target_language)
    return jsonify({'translated_text': translated_text})

@app.route('/bg.mp4')
def get_bg_video():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'bg.mp4')

def translate_text(text, target_language):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'contents': [
            {
                'parts': [
                    {'text': f'Translate the following text to {target_language}: {text}'}
                ]
            }
        ]
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            result = response.json()
            candidates = result['candidates']
            if candidates:
                return candidates[0]['content']['parts'][0]['text']
            else:
                return 'No translation generated'
        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"Response JSON: {result}")
            return 'Failed to process request'
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.json()}")
        return 'Failed to process request'

if __name__ == '__main__':
    app.run(debug=True)