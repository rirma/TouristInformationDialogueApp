import wave
import sys
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

class Wave():
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        wave_file = wave.open(self.in_file,"r") #Open
        self.params = wave_file.getparams()
        self.N = wave_file.getnframes() #サンプル数
        self.dt = 1/wave_file.getframerate() #サンプリング間隔
        self.freq = np.linspace(0, 1.0/self.dt, self.N)  # 周波数軸
        wave_file.close()

    def wave2numpy(self):
        """読み込み作業"""
        wave_file = wave.open(self.in_file,"r") #Open

        #print(wave_file.getnchannels()) #モノラルorステレオ
        #print(wave_file.getframerate()) #サンプリング周波数
        #print(wave_file.getnframes()) #フレームの総数

        #print(wave_file.getparams())

        x = wave_file.readframes(wave_file.getnframes()) #frameの読み込み
        x = np.frombuffer(x, dtype= "int16") #numpy.arrayに変換
        wave_file.close()
        
        return x

    def save_numpy2wave(self, x):
        """書き込み作業"""
        write_wave = wave.Wave_write(self.out_file)
        write_wave.setparams(self.params)
        write_wave.writeframes(x)
        write_wave.close()

    def fourier_trans(self, x, high_cut = 2500, low_cut = 300):
        # 高速フーリエ変換（周波数信号に変換）
        F = np.fft.fft(x)

        # 配列Fをコピー
        F2 = F.copy()

        F2[(self.freq > high_cut)] = 0
        F2[(self.freq < low_cut)] = 0

        # 高速逆フーリエ変換（時間信号に戻す）
        f2 = np.fft.ifft(F2)

        new_x = np.array(f2, dtype= "int16")
        return new_x

if __name__ == "__main__":
    treat_wave = Wave('../sound/20200926112840.wav', '../sound/filtered2.wav')
    x = treat_wave.wave2numpy()

    new_x = treat_wave.fourier_trans(x)

    treat_wave.save_numpy2wave(new_x)