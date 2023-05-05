from flask import Flask, send_file
from flask_cors import CORS,cross_origin
from flask import request
from flask import jsonify
#from gtts import gTTS
import boto3
from botocore.exceptions import ClientError
import os
import firebase_admin
from firebase_admin import credentials, storage
from pydub import AudioSegment
from google.cloud import storage
import tempfile
import subprocess
import pyrebase
import requests
from flask_ngrok import run_with_ngrok
#from pyngrok import ngrok
app = Flask(__name__)


CORS(app)
#run_with_ngrok(app)

# http_tunnel = ngrok.connect()
# print(http_tunnel) 

config = {
  'apiKey': "AIzaSyDM0PhsTdKFoAaUpFrqOjVT1j7LJo9HPHU",
  'authDomain': "learnit-d0064.firebaseapp.com",
  'databaseURL': "https://learnit-d0064-default-rtdb.firebaseio.com",
  'projectId': "learnit-d0064",
  'storageBucket': "learnit-d0064.appspot.com",
  'messagingSenderId': "170403956115",
  'appId': "1:170403956115:web:82628f9f574f0b7c04d466"
}

words = {
    'Olá ':'Hello',
    'Amor': 'Love',
    'Felicidade':'Happiness',
    'Gato':'cat',
    'Cão' : 'Dog',
    'Sim':'Yes',
    'Obrigado':'Thank You',
    'amanhã':'Tomorrow',
    'Ontem':'Yesterday',
    'Seguendo':'Second',
    'Ponte':'Bridge',
    'Rua':'Street',
    'Suco':'Juice',
    'Bolo':'cake',
    'bom':'Good',
    'frio':'cold',
}



firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# cred = credentials.Certificate('learnit-d0064-firebase-adminsdk-r10th-b02c5c4f97.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'learnit-d0064.appspot.com'})
# bucket = storage.bucket()
@app.route('/hi')
def send():
    return jsonify({'hi':'hi'})

@app.route('/convert',methods=['POST'])
def convert():
    
    url = request.form.get('firebase-link')
    word = request.form.get('word')

    url1 = "https://thefluentme.p.rapidapi.com/post"

    querystring1 = {"page":"1","per_page":"10"}

    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "a975cce100msh85e7f0a286a7052p170016jsn7d628e53b9fa",
	"X-RapidAPI-Host": "thefluentme.p.rapidapi.com"
}

    response1 = requests.get(url1, headers=headers, params=querystring1)

    print(response1.json()[1]['posts'])
    pid = 'P32328112'
    for w in response1.json()[1]['posts']:
        if w['post_content'] == word:
            pid = w['post_id']
        #print("Word: "+w['post_content']+' : post_id: '+w['post_id'])
    # for pword in word_dict:
    #     if pword == word:
    #         pid = word_dict[pword]
    r = requests.get(url, allow_redirects=True)
    open('hello.mp3', 'wb').write(r.content)

    # assign files
    input_file = "hello.mp3"
    output_file = "hello_.wav"

    # convert mp3 file to wav file
    sound = AudioSegment.from_mp3(input_file)
    sound.export(output_file, format="wav")

    path_on_cloud = 'hello.wav'
    path_local = 'hello_.wav'

    res = storage.child(path_on_cloud).put(path_local)
    firebase_url = 'https://firebasestorage.googleapis.com/v0/b/learnit-d0064.appspot.com/o/hello.wav?alt=media&token='+res['downloadTokens']

    #blob = bucket.blob('gs://learnit-d0064.appspot.com/hello.wav')
    # blob = bucket.blob('hello.wav')
    # url = blob.get_url()
    # print('Download URL:', url)

    url = "https://thefluentme.p.rapidapi.com/score/"+pid

    querystring = {"scale":"100"}

    payload = { "audio_provided": firebase_url }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    print(response.json())
    result = response.json()
    score = result[2]['word_result_data'][0]['points']

    return jsonify({'score':score})

@app.route('/draw',methods=['POST'])
def draw():
    promptPT = request.form.get('promptPT')
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": promptPT,
        "source": "pt",
        "target": "en"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "f1e3b6cb95mshe6249c40abcce80p1fc857jsnf31428aeaa50",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    r = requests.post(
        "https://api.deepai.org/api/stable-diffusion",
        data={
            'text': response.json()['data']['translations']['translatedText'],
        },
        headers={'api-key': 'f5934187-68d4-4360-b835-850dcb9b5703'}
    )
    print(r.json()['output_url'])
    return jsonify({'translated_text':r.json()['output_url']})

if __name__ == '__main__':
    app.run(port=5000)

