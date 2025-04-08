from flask import Flask, request, send_file, jsonify
from gtts import gTTS
from flask_cors import CORS
import uuid
import os

# תרגום
from googletrans import Translator

app = Flask(__name__)
CORS(app)

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
    tts = gTTS(text=text, lang='am')  # שפה: אמהרית
    tts.save(filename)

    response = send_file(filename, mimetype='audio/mpeg')
    os.remove(filename)
    return response

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translator = Translator()
        result = translator.translate(text, src='he', dest='am')
        return jsonify({
            "original": text,
            "translated": result.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
