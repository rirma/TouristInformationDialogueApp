from pydub import AudioSegment as am
import numpy as np

class ConvertAudio:
    def convert_rate(self, in_file, out_file, file_type = 'wav', rate=16000):
        sound = ''
        if file_type == 'wav':
            sound = am.from_wav(in_file)
        elif file_type == 'mp3':
            print(in_file)
            sound = am.from_mp3(in_file)
        sound = sound.set_frame_rate(rate)
        sound.export(out_file, format='wav')
        print('convert ok')
    def convert_sound_rate(self, in_file, rate=16000):
        return in_sound.set_frame_rate(rate)
    def wav2numpy(self, in_file):
        sound = am.from_wav(in_file)
        return np.array(sound.get_array_of_samples(), dtype='uint16')
    def mp2numpy(self, in_file):
        sound = am.from_mp3(in_file)
        return np.array(sound.get_array_of_samples(), dtype='uint16')
    def read_byte_file(self, in_file):
        fr = open(in_file, 'rb')
        datas = []
        while True:
            data = fr.read(1)
            datas.append(data)
            if len(data) == 0:
                break

        fr.close()
        datas = [int.from_bytes(datas[i], 'big') for i in range(len(datas))]
        return datas