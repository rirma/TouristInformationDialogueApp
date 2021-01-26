import io
import os
import subprocess

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
import requests
import json

from apiclient.discovery import build

class GoogleCloudController():
    def __init__(self, cloud_key_json, api_key='', sample_rate=16000, lang_code = 'ja-JP'):
        self.sample_rate = sample_rate
        self.lang_code = lang_code
        self.api_key = api_key
        if cloud_key_json != '':
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cloud_key_json

        if api_key != '':
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    def speech2text(self, file_path):
        # Instantiates a client
        client = speech.SpeechClient()

        # The name of the audio file to transcribe
        file_name = file_path

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.sample_rate,
            language_code=self.lang_code)

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        result_li = []
        for result in response.results:
            result_li.append(format(result.alternatives[0].transcript))

        return result_li
    
    def reverse_geo_cording(self, lat, lng):
        param = {}
        json_result = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+ str(lat) + ',' + str(lng) + '&key=' + self.api_key)
        result = json.loads(json_result.text.replace("'",'"'))
        return result['results'][0]['address_components']
    
    def get_youtube_url(self, query, order = 'relevance'):
        search_response = self.youtube.search().list(
            part='snippet',
            #検索したい文字列を指定
            q=query,
            order=order,
            type='video',
        ).execute()

        videoId = search_response['items'][0]['id']['videoId']
        url = 'https://www.youtube.com/watch?v=' + videoId
        return url