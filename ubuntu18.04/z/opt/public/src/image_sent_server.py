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

async_mode = None
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode = async_mode)
thread = None

index = 0
main = Main()
converter = ConvertAudio()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # アップロード後のページに転送
            return redirect(url_for('uploaded_file', filename=filename))

    res_text = '<!doctype html>'
    res_text += '<html>'
    res_text += '<body>'
    res_text += '<head>'
    res_text += '<meta charset="UTF-8">'
    res_text += '<title>'
    res_text += 'upload file'
    res_text += '</title>'
    res_text += '</head>'
    res_text += '<body>'
    res_text += '<h1>please upload your file<h1>'
    res_text += '<form method = post enctype = multipart/form-data>'
    res_text += '<input type=file name = file>'
    res_text += '<input type = submit value = Upload>'
    res_text += '</form>'
    res_text += '</body>'
    res_text += '</html>'
    return res_text

if __name__ == "__main__":
    #app.run(debug=False, port=80)
    #socketio.run(app, host='0.0.0.0', debug=False, port=8000)
    #serve(app, host='192.168.33.10', port=8000)
    #app.run(host='0.0.0.0', port=80)
    waitress.serve(app, host='10.0.30.3', port=8000)
