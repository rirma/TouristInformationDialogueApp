
import sys
from pprint import pprint


filename = sys.argv[1]

wavfile = open(filename, 'rb')

wav_header = {}

wav_header['riff_chunk_id'] = wavfile.read(4).decode('ascii')
wav_header['riff_chunk_size'] = int.from_bytes(wavfile.read(4), 'little')
wav_header['riff_form_type'] = wavfile.read(4).decode('ascii')
wav_header['fmt_chunk_id'] = wavfile.read(4).decode('ascii')
wav_header['fmt_chunk_size'] = int.from_bytes(wavfile.read(4), 'little')
wav_header['fmt_wave_format_type'] = int.from_bytes(wavfile.read(2), 'little')
wav_header['fmt_channel'] = int.from_bytes(wavfile.read(2), 'little')
wav_header['fmt_samples_per_sec'] = int.from_bytes(wavfile.read(4), 'little')
wav_header['fmt_bytes_per_sec'] = int.from_bytes(wavfile.read(4), 'little')
wav_header['fmt_block_size'] = int.from_bytes(wavfile.read(2), 'little')
wav_header['fmt_bits_per_sample'] = int.from_bytes(wavfile.read(2), 'little')
wav_header['data_chunk_id'] = wavfile.read(4).decode('ascii')
wav_header['data_chunk_size'] = int.from_bytes(wavfile.read(4), 'little')

pprint(wav_header)


'''
from main import Main
from translate import Translate

def main():
    main = Main()
    trans = Translate()
    voice_text = '金曜日の枚方市の天気は？'
    where, when, what = main.analyze_whether_text(voice_text)
    where = [where.replace('市', '')]
    lat = 34.5045
    lng = 135.4227
    if len(where) == 0 and lat != 0 and lng != 0:
        data = main.gc_controller.reverse_geo_cording(lat, lng)
        for d in data:
            if 'locality' in d['types']:
                where.append(d['short_name'])
            if 'administrative_area_level_1' in d['types']:
                where.append(d['short_name'])

    for data in where:
        while True:
            try:
                data = trans.trans(data, 'ja', 'en').text
                break
            except Exception as e:
                pass
        res = main.create_weather_res(data, when, what)
    print(res)

if __name__== '__main__':
    main()
'''
'''
def create_return_state(state, value_name, value_content):
    state_dic = {}
    state_array = state.split(' ')
    for data in state_array:
        values = data.split('=')
        state_dic[values[0]] = values[1]
    state_dic[value_name] = value_content
    return_state = ''
    for key in state_dic:
        if len(return_state) == 0:
            return_state += key + '=' + state_dic[key]
        else:
            return_state += ' ' + key + '=' + state_dic[key]
    return return_state

state = 'a=12345 i=6789'
text = create_return_state(state, 'a', 'aiai')
print('#' + text + '#')
'''