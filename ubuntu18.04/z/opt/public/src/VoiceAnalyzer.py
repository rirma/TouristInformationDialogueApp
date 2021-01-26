# ライブラリの読込
import pyaudio
import wave
import numpy as np
from datetime import datetime
import subprocess

class VoiceAnalyzer:
    def __init__(self, chunk = 1024, format = pyaudio.paInt16, channels = 1, rate = 16000, record_seconds = 2, threshold = 0.1):
        self.chunk = chunk
        self.FORMAT = format
        self.CHANNELS = channels
        self.RATE = rate
        self.RECORD_SECONDS = record_seconds
        self.threshold = threshold

    def start_record(self, dir_name = '../sound/'):
        if dir_name[-1] != '/':
            dir_name += '/'
        # 音の取込開始
        p = pyaudio.PyAudio()
        stream = p.open(format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            frames_per_buffer = self.chunk
        )

        while True:
            # 音データの取得
            data = stream.read(self.chunk)
            # ndarrayに変換
            x = np.frombuffer(data, dtype="int16") / 32768.0

            # 閾値以上の場合はファイルに保存
            if x.max() > self.threshold:
                filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".wav"
                print('start record')

                # RECORD_SECONDS秒の音データを取込
                all = []
                all.append(data)
                for i in range(0, int(self.RATE / self.chunk * int(self.RECORD_SECONDS))):
                    data = stream.read(self.chunk)
                    all.append(data)
                data = b''.join(all)

                # 音声ファイルとして出力
                out = wave.open(dir_name + filename,'w')
                out.setnchannels(self.CHANNELS)
                out.setsampwidth(2)
                out.setframerate(self.RATE)
                out.writeframes(data)
                out.close()

                print("Saved.")
                break

        stream.close()
        p.terminate()

        return filename

    def analyze_voice(self, file_path):
        res = ''
        try:
            res = subprocess.check_output('echo ' + file_path + ' | bash julius-start.sh', shell = True, encoding = 'utf-8')
        except:
            print("Error.")

        res = res.splitlines()
        find = False
        sentence = ''
        sub_sentence = ''
        for val in res:
            if 'sentence1:' in val:
                sentence = val
                find = True
            elif 'pass1_best:' in val:
                sub_sentence = val
        sentence = sentence.replace('sentence1:', '')
        sentence = sentence.replace(' ', '')
        sub_sentence = sub_sentence.replace('pass1_best:', '')
        sub_sentence = sub_sentence.replace(' ', '')

        if find:
            return sentence
        return sub_sentence

if __name__ == "__main__":
    record = VoiceAnalyzer(rate=16000)
    sound_file = record.start_record()
    print(sound_file)
    print(record.analyze_voice('../sound/' + sound_file))