from gtts import gTTS
import wave
import sys
from mutagen.mp3 import MP3 as mp3
import pygame
import time
from datetime import datetime
from pydub import AudioSegment as am

class SoundMP3:
    def __init__(self, registerd_path, dev_path):
        if registerd_path[-1] != '/':
            registerd_path += '/'
        if dev_path[-1] != '/':
            dev_path += '/'

        self.registerd_path = registerd_path
        self.dev_path = dev_path

    def create_sound(self, create_str, mode='mp3'):
        hoge = gTTS(create_str, lang='ja')
        filename = datetime.today().strftime("%Y%m%d%H%M%S")
        hoge.save(self.dev_path + filename + '.mp3')
        if(mode == 'wav'):
            sound = am.from_mp3(self.dev_path + filename + '.mp3')
            sound.export(self.dev_path + filename + '.wav', format="wav")
            return filename + '.wav'
        
        return filename + '.mp3'

    def sound_registered_mp3(self, file_name):   
        filename = self.registerd_path + file_name #再生したいmp3ファイル
        pygame.mixer.init()
        pygame.mixer.music.load(filename) #音源を読み込み
        mp3_length = mp3(filename).info.length #音源の長さ取得
        pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        pygame.mixer.music.stop() #音源の長さ待ったら再生停止

    def sound_dev_mp3(self, file_name):   
        filename = self.dev_path + file_name #再生したいmp3ファイル
        pygame.mixer.init()
        pygame.mixer.music.load(filename) #音源を読み込み
        mp3_length = mp3(filename).info.length #音源の長さ取得
        pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
        time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
        pygame.mixer.music.stop() #音源の長さ待ったら再生停止