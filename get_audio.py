import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from pathlib import Path
from time import sleep

load_dotenv()

def generate_mp3(youtube_link):
    url = "https://youtube-to-mp315.p.rapidapi.com/download"
    apikey = os.getenv("YOUTUBE_TO_MP3_APIKEY")
    querystring = {"url":youtube_link,"format":"mp3"}

    payload = {}
    headers = {
        "x-rapidapi-key": apikey,
        "x-rapidapi-host": "youtube-to-mp315.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    result ={} 
    response = requests.post(url, json=payload, headers=headers, params=querystring)  
    if response.status_code == 200:  
        result['id'] = response.json().get('id')
        result['downloadUrl'] = response.json().get('downloadUrl')
        print(result.get('downloadUrl'))
        #{'quality': 0, 'startTime': None, 'id': '5e1e0b69-b7b4-400f-bbf5-055189b5494f', 'downloadUrl': 'http://217.69.15.145/5e1e0b69-b7b4-400f-bbf5-055189b5494f.mp3', 'endTime': None, 'status': 'CONVERTING', 'startAt': '19/10/2024 14:02:49', 'title': None, 'retry': 0, 'endAt': None, 'format': 'MP3'}
    else: 
        print('Request failed. ' + response.text)
    return result

def check_status(id):
    apikey = os.getenv("YOUTUBE_TO_MP3_APIKEY")
    headers = {
        "x-rapidapi-key": apikey,
        "x-rapidapi-host": "youtube-to-mp315.p.rapidapi.com",
    }
    url = f"https://youtube-to-mp315.p.rapidapi.com/status/{id}"
    response = requests.get(url, headers=headers)
    #'{"quality":0,"startTime":null,"id":"5e1e0b69-b7b4-400f-bbf5-055189b5494f","downloadUrl":"http:\\/\\/217.69.15.145\\/5e1e0b69-b7b4-400f-bbf5-055189b5494f.mp3","endTime":null,"status":"EXPIRED","startAt":"19\\/10\\/2024 14:02:49","title":"Loading an audio file using Fetch - Web Audio API","retry":0,"endAt":"19\\/10\\/2024 14:03:52","format":"MP3"}'
    return(response)

def download_mp3(downloadUrl):
    response = requests.post(url=downloadUrl)
    filename =  f"audio_{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp3"
    cwdpath = Path(os.getcwd())
    filepath=f'{cwdpath.parent.parent}/{filename}'
    print(type(response.content))
    print(len(response.content))
    with open(filepath,'wb') as f:
        f.write(response.content)
    print(f"File {filepath} ready.")
    return response

test_video_url = 'https://www.youtube.com/watch?v=3NgVlAscdcA&list=PLMPgoZdlPumc_llMSynz5BqT8dTwr5sZ2&index=1'
res = generate_mp3(test_video_url)
# one_generated_file='http://149.28.171.55/13e17be1-9293-4a86-9a56-2848663127b7.mp3'
id = res.get('id')
if id:
    i=0
    while(status != 'AVAILABLE'):
        sleep(2)
        res = check_status(id)
        i+=1
        if res.status_code == 200:
            status = res.json().get('status')
        if i>10:
            break
    if status == 'AVAILABLE':
        r = download_mp3(durl)
        print(r.text)

else:
    print('Audio generation failed: ' + res.text)
# r = download_mp3('http://217.69.15.145/5e1e0b69-b7b4-400f-bbf5-055189b5494f.mp3')
# r = check_status('5e1e0b69-b7b4-400f-bbf5-055189b5494f')
# r = check_status('13e17be1-9293-4a86-9a56-2848663127b7')

