import os
import uuid
import requests
from flask import Flask, request
import torch
from transformers import pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-tiny.en",
  chunk_length_s=30,
  device=device,
)

app = Flask(__name__)

@app.route('/audio', methods=['POST'])
def upload_audio():
    audio = request.files['audio']
    filename = str(uuid.uuid4()) + os.path.splitext(audio.filename)[1]
    audio.save(os.path.join('audios', filename))
    # transcribe audio file
    transcript = pipe(os.path.join('audios', filename))["text"]
    print("transcript : " + transcript)
    # send transcript to Rasa server
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': transcript}).json()
    # extract response text from Rasa server response
    response_text = rasa_response[0]['text']
    print("response_text : " + response_text)
    # return JSON response
    return {'user_transcript': transcript, 'ai_response': response_text}

@app.route('/message', methods=['POST'])
def send_message():
    message = request.form['message']
    # send transcript to Rasa server
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={'message': message}).json()
    # extract response text from Rasa server response
    response_text = rasa_response[0]['text']
    print("response_text : " + response_text)
    # return JSON response
    return {'response': response_text}

if __name__ == '__main__':
    app.run(debug=True , port=7000)