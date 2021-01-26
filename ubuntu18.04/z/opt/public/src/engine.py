#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, session
import json
from flask_socketio import SocketIO
import sys
from flask_cors import CORS
import numpy as np
import wave
from main import Main, Task
from datetime import datetime
from AudioConverter import ConvertAudio
import requests
import waitress
import sys

async_mode = None
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode = async_mode)
thread = None

index = 0
main = Main()
converter = ConvertAudio()

voice_analyze_mode = sys.argv[1]

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/", methods=['POST'])
def iDeea():
    global index, main, convert
    result = {}
    if request.method == "POST":
        data = request.data.decode('utf-8')
        data = json.loads(data)
        lat = 0
        lng = 0
        if data['gps_latitude'] != 0:
            lat = data['gps_latitude']
        if data['gps_longitude'] != 0:
            lng = data['gps_longitude']
        voice_string = ''
        if data['input_mode'] == 'voice':
            recordData = np.array(data['recordData'], dtype='uint8')
            recordData = recordData[44:]
            print(len(recordData))
            recordData = np.frombuffer(recordData, dtype='int16')
            print(len(recordData))
            print(type(recordData[0]))

            # 書き出し
            sound_file = '../sound/original/data_' + datetime.today().strftime("%Y%m%d%H%M%S") + '.wav'
            ww = wave.open(sound_file, 'w')
            ww.setnchannels(1)
            ww.setsampwidth(2)
            ww.setframerate(16000)
            ww.writeframes(recordData)
            ww.close()

            #音声処理
            if data['task'] == 'start_listen':
                voice_string = main.sound_to_str(sound_file, 'julius')
                print(voice_string)
            else:
                if voice_analyze_mode == 'julius':
                    voice_string = main.sound_to_str(sound_file, 'julius')
                    print(voice_string)
                else:
                    voice_string = main.sound_to_str(sound_file, 'google')
                    print(voice_string)
        else:
            voice_string = data['content']

        res, task, state = main.return_result(voice_string, data, lat, lng)

        result['submitted'] = voice_string

        if len(res) != 0:
            out_file = '../sound/system_sound/dev/' + main.system_sound.create_sound(res)

            data = converter.mp2numpy(out_file)
            data = list(np.frombuffer(data, dtype='uint8'))
            data = [int(val) for val in data]
            result['serif'] = res
            result['audio'] = data
            result['state'] = state
            result['task'] = task

    return json.dumps(result)


if __name__ == "__main__":
    waitress.serve(app, host='0.0.0.0', port=8000)