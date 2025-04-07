from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "gTTS API is running."

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang='am')  # תוכל לשנות שפה כאן
    tts.save(filename)

    response = send_file(filename, mimetype='audio/mpeg')
    os.remove(filename)
    return response

if __name__ == '__main__':
    app.run()
