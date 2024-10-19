import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from pathlib import Path

load_dotenv()

def generate_mp3(youtube_link):
    url = "https://youtube-to-mp315.p.rapidapi.com/download"
    apikey = os.get_env("YOUTUBE_TO_MP3_APIKEY")
    querystring = {"url":youtube_link,"format":"mp3"}

    payload = {}
    headers = {
        "x-rapidapi-key": apikey,
        "x-rapidapi-host": "youtube-to-mp315.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)    
    print(response.json())
    #{'quality': 0, 'startTime': None, 'id': '5e1e0b69-b7b4-400f-bbf5-055189b5494f', 'downloadUrl': 'http://217.69.15.145/5e1e0b69-b7b4-400f-bbf5-055189b5494f.mp3', 'endTime': None, 'status': 'CONVERTING', 'startAt': '19/10/2024 14:02:49', 'title': None, 'retry': 0, 'endAt': None, 'format': 'MP3'}
    return response.json().get('downloadUrl')

def download_mp3(downloadUrl):
    response = requests.post(url=downloadUrl)
    filename =  f"audio_{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp3"
    cwdpath = Path(os.getcwd())
    filepath=f'{cwdpath.parent.parent}/{filename}'
    #filepath='simple.mp3'
    with open(filepath,'wb') as f:
        f.write(response.content)
    print(f"File {filepath} ready.")
    return response

r = download_mp3('http://217.69.15.145/5e1e0b69-b7b4-400f-bbf5-055189b5494f.mp3')
type(r)
print('wait here')
