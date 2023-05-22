import os
import uuid
import requests
from flask import Flask, request , send_from_directory
import torch
from transformers import pipeline
from elevenlabs import generate, play, set_api_key , save

set_api_key("9fed84e04fd3592c7a9178adc97c6552")


device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-tiny.en",
  chunk_length_s=30,
  device=device,
)

app = Flask(__name__)

@app.route('/ai_audios/<path:filename>')
def download_file(filename):
    return send_from_directory('ai_audios', filename)

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
    audio = generate(
        text= response_text,
        voice="Sam"
    )
    response_audio_path = str(uuid.uuid4()) + ".mp3"
    full_path = os.path.join('ai_audios', response_audio_path)
    save(audio, full_path)
    print("response_text : " + response_text)
    # return JSON response
    return {'user_transcript': transcript, 'ai_response': response_text , 'ai_audio_path' : 'ai_audios/'+response_audio_path}

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
    app.run(debug=True , port=7000 , host= '192.168.1.4')