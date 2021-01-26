from VoiceAnalyzer import VoiceAnalyzer
from noise_remove import Wave
from SystemSound import SoundMP3
from GoogleCloudController import GoogleCloudController
import time
from enum import Enum, auto
from translate import Translate
from OpenWeatherMapForecast import Forecast
import datetime
from pytz import timezone
import MeCab
import copy
from JalanController import jalan_controller
import jaconv
import subprocess

class Task(Enum):
    greeting = auto()
    default = auto()
    weather = auto()
    news = auto()
    hear_youtube = auto()
    player_stop = auto()
    listen_drive_mode_content = auto()
    listen_kankou_where = auto()
    listen_food_where = auto()
    talk_kankou_list = auto()
    about_hearing = auto()
    talk_about_hearing = auto()
    navigate = auto()
    talk_food_shop = auto()
    talk_famous = auto()

class Main:
    def __init__(self):
        self.system_sound = SoundMP3('../sound/system_sound/registerd', '../sound/system_sound/dev')
        self.trans = Translate()
        self.gc_controller = GoogleCloudController('', api_key = '')
        self.translater = Translate()
        self.forecast = Forecast('')
        self.mecab = MeCab.Tagger("-d /home/linuxbrew/.linuxbrew/lib/mecab/dic/mecab-ipadic-neologd")
        self.temporary_data = ''
        self.return_state = {}
        self.jalan_controller = jalan_controller()
    
    def analyze_text_by_juman(self, text):
        res = subprocess.check_output('python3 JumanAnalyzer.py ' + text, shell = True, encoding = 'utf-8')
        res = res.split('\n')
        result_list = []
        for item in res:
            result_list.append(item.split(','))
        return result_list[:-1]
    
    def kanji2number(self, text):
        text = text.replace('一', '1')
        text = text.replace('二', '2')
        text = text.replace('三', '3')
        text = text.replace('四', '4')
        text = text.replace('五', '5')
        text = text.replace('六', '6')
        text = text.replace('七', '7')
        text = text.replace('八', '8')
        text = text.replace('九', '9')
        text = text.replace('十', '')
        text = text.replace('百', '')
        return text
    
    def to_hiragana(self, text):
        word1 = text
        change_word1 = jaconv.kata2hira(word1)
        return change_word1

    def set_str2state(self, state):
        state_list = state.split(' ')
        for item in state_list:
            item_list = item.split('=')
            if len(item_list) == 2:
                self.return_state[item_list[0]] = item_list[1]

    def get_state(self):
        result = ''
        for key in self.return_state:
            result += ' ' + str(key) + '=' + str(self.return_state[key])
        return result

    def analyze_text(self, text):
        return self.mecab.parseToNode(text)
    
    def pickup_where(self, node):
        where = ''
        is_first = True
        while node:
            word = node.surface
            hinshi = node.feature.split(",")[2]
            if hinshi == '地域':
                if is_first:
                    where += word
                    is_first = False
                else:
                    where += '　' + word
            node = node.next
        return where

    def analyze_whether_text(self, original_text):
        node = self.analyze_text(original_text)
        where = ''
        when = ''
        what = ''
        where = self.pickup_where(node)

        if '今日' in original_text:
            when = '今日'
        elif '明日' in original_text:
            when = '明日'
        elif '明後日' in original_text:
            when = '明後日'
        elif '曜日' in original_text:
            index = original_text.index('曜日')
            when = original_text[index-1]
        elif '今週' in original_text:
            when = '今週'
        
        if '天気' in original_text:
            what = '天気'
        if '詳細' in original_text:
            what = '詳細'
        
        return where, when, what

    def match_start_str(self, validation_str):
        start_li = ['ええと', 'えっと', '絵本', 'エド', '五', 'エコ', 'Ｏ', 'でも', 'ゼロ', 'と。', 'Ｚ', 'それと', '是と', '図と']
        for val in start_li:
            if val in validation_str:
                return True
        return False

    def sound_to_str(self, sound_file, mode):
        return_text = ''

        if mode == 'julius':
            analyzer = VoiceAnalyzer(rate = 16000)
            return_text = analyzer.analyze_voice(sound_file)
        elif mode == 'google':
            result_text = self.gc_controller.speech2text(sound_file)
            print(result_text)
            if len(result_text) != 0:
                return_text = result_text[0]
        else:
            return_text = ''

        return return_text

    def recording(self, rate = 16000, threshhold = 0.15, record_seconds = 1, filtering = True, mode = 'julius'):
        sound_dir = '../sound/original/'
        filtered_dir = '../sound/filtered/'

        analyzer = VoiceAnalyzer(rate = rate, threshold = threshhold, record_seconds = record_seconds)
        sound_file = analyzer.start_record(sound_dir) #開始させるボイス受付

        if filtering:
            treat_wave = Wave(sound_dir + sound_file, filtered_dir + sound_file)
            x = treat_wave.wave2numpy()
            x = treat_wave.fourier_trans(x, 10000)
            treat_wave.save_numpy2wave(x)

            return self.sound_to_str(treat_wave.out_file, mode)

        return self.sound_to_str(sound_dir+sound_file, mode)

    def recognize_call(self, call_str = 'Z'):
        while True:
            rec_str = self.recording() #入力受付け
            if self.match_start_str(rec_str):
                return
            else:
                print(rec_str)
    
    def get_where_foodname(self, rec_str):
        text = self.analyze_text_by_juman(rec_str)
        where = ''
        food_name = ''

        noun_result = []
        noun_list = []
        for item in text:
            if item[4] == '地名':
                where = item[0]
            if item[3] == '名詞':
                noun_list.append(item)
            elif len(noun_list) != 0:
                noun_result.append(noun_list)
                noun_list = []

        for result in noun_result:
            is_food = False
            for item in result:
                if '食べ物' in item[7]:
                    is_food = True
                    break
            if is_food:
                if len(food_name) != 0:
                    food_name += '　'
                for item in result:
                    food_name += item[0]
        self.return_state['where'] = where
        self.return_state['food_name'] = food_name

    def classify_tasks(self, rec_str, user_state):
        self.temporary_data = self.analyze_text(rec_str)
        if '有名なもの' in rec_str or '有名な物' in rec_str:
            node = self.temporary_data
            where = self.pickup_where(node)
            if len(where) != 0:
                self.return_state['where'] = where

            return Task.listen_drive_mode_content
        elif '観光地' in rec_str:
            node = self.temporary_data
            where = self.pickup_where(node)
            
            if len(where) != 0:
                self.return_state['where'] = where
                return Task.talk_kankou_list
            else:
                return Task.listen_kankou_where
        elif '名物' in rec_str or '食べ物' in rec_str:
            node = self.temporary_data
            where = self.pickup_where(node)
            
            if len(where) != 0:
                self.return_state['where'] = where
                return Task.talk_kankou_list
            else:
                return Task.listen_food_where
        elif 'について教えて' in rec_str:
            return Task.about_hearing
        elif '行きたい' in rec_str or '案内して' in rec_str:
            return Task.navigate
        elif '食べたい' in rec_str:
            self.get_where_foodname(rec_str)
            return Task.talk_food_shop
        elif '有名な' in rec_str:
            return Task.talk_famous

        if 'おはよう' in rec_str:
            return Task.greeting
        elif 'こんにちは' in rec_str:
            return Task.greeting
        elif 'こんばんは' in rec_str:
            return Task.greeting
        elif 'ストップ' in rec_str:
            return Task.player_stop
        elif '止めて' in rec_str:
            return Task.player_stop
        elif '消して' in rec_str:
            return Task.player_stop
        elif '閉じて' in rec_str:
            return Task.player_stop
        elif '天気' in rec_str:
            return Task.weather
        elif 'ニュース' in rec_str:
            return Task.news
        elif 'YouTube' in rec_str:
            return Task.hear_youtube

        return Task.default

    def create_greeting_res(self, rec_str):
        if 'おはよう' in rec_str:
            return 'おはよう'
        elif 'こんにちは' in rec_str:
            return 'こんにちは'
        elif 'こんばんは' in rec_str:
            return 'こんばんは'
        return 'ごきげんよう'

    def create_weather_res(self, where, when, what):
        return_text = ''
        if when == '明日' or when == '今日' or when == '明後日' or when in ['月', '火', '水', '木', '金', '土', '日']:
            forecastDatetime = []
            weatherDescription = []
            temperature = []
            dt_now = datetime.datetime.now()
            forecast_day_diff = 0
            if when == '今日':
                pass
            elif when == '明日':
                forecast_day_diff = 1
            elif when == '明後日':
                forecast_day_diff = 2
            else:
                week_li = ['月', '火', '水', '木', '金', '土', '日']
                weekday = datetime.date.today().weekday()
                forecast_weekday = week_li.index(when)
                forecast_day_diff = (forecast_weekday - weekday) % 7
            dt_now += datetime.timedelta(days=forecast_day_diff)

            data = self.translater.trans(where, 'ja', 'en')
            if data != None:
                data = data.text
            else:
                return 'すみません。翻訳時にエラーが起こりました。'
            print(data, when, what)
            forecastData = self.forecast.forecast_week(data)
            if 'list' not in forecastData:
                return 'where is invalid'
            for item in forecastData['list']:
                forecast_time = timezone(
                    'Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))

                if dt_now.day != forecast_time.day:
                    continue
                else:
                    forecastDatetime.append(forecast_time)
                    weatherDescription.append(item['weather'][0]['main'])
                    temperature.append(item['main']['temp'])
            print(forecastDatetime)
            print(weatherDescription)
            max_temp = int(max(temperature))
            min_temp = int(min(temperature))
            clear = 0
            cloud = 0
            lain = 0
            morning = ''
            afternoon = ''
            for data in weatherDescription[:4]:
                if data == 'Clear':
                    clear += 1
                elif data == 'Clouds':
                    cloud += 1
                else:
                    lain += 1
            if clear > cloud and clear > lain:
                morning = '晴れ'
            elif cloud >= clear and cloud > lain:
                morning = '曇り'
            else:
                morning = '雨'

            clear = 0
            cloud = 0
            lain = 0
            for data in weatherDescription[4:]:
                if data == 'Clear':
                    clear += 1
                elif data == 'Clouds':
                    cloud += 1
                else:
                    lain += 1
            if clear > cloud and clear > lain:
                afternoon = '晴れ'
            elif cloud >= clear and cloud > lain:
                afternoon = '曇り'
            else:
                afternoon = '雨'

            weather_text = ''
            if morning == afternoon:
                weather_text = morning
            else:
                weather_text = morning + 'のち' + afternoon
            day = when
            if when in ['月', '火', '水', '木', '金', '土', '日']:
                day += '曜日'
            return_text = '{0}の{1}の天気は{2}、最高気温{3}度、最低気温{4}度です。'.format(
                day, where, weather_text, max_temp, min_temp
            )
        return return_text
    
    def create_news_res(self, voice_string):
        news_string_index = voice_string.find('ニュース')
        voice_string = voice_string[:news_string_index]
        query = 'ニュース '
        node = self.analyze_text(voice_string)
        while node:
            word = node.surface
            hinshi = node.feature.split(",")[0]
            if hinshi == '助詞':
                pass
            else:
                query += word
            node = node.next
        url = self.gc_controller.get_youtube_url(query, order = 'relevance')
        return url

    def create_food_spot_res(self, task_name, voice_string):
        res = ''
        task = ''
        if task_name == 'hear drive content':
            if '食べ物' in voice_string or 'たべもの' in voice_string or '食い物' in voice_string or '名物' in voice_string:
                where_analyze = self.analyze_text_by_juman(self.return_state['where'])
                parent_where = where_analyze[0][7].split(' ')[1].split(':')[2]
                parent_where = parent_where.replace('都', '').replace('道', '').replace('府', '').replace('県', '')
                where = where_analyze[0][0]
                where, spot_name_list, spot_url_list = self.jalan_controller.get_specialty_food(where, parent_where)
                read_out_values = min(5, len(spot_name_list))
                for i in range(len(spot_name_list)):
                    self.return_state['spot_name_' + str(i)] = spot_name_list[i].replace(' ', '　')
                    self.return_state['spot_url_' + str(i)] = spot_url_list[i]
                self.return_state['previous'] = 'read_food'
                self.return_state['read_out_values_first'] = 0
                self.return_state['read_out_values_last'] = read_out_values
                res = where + 'で有名な食べ物を' + str(read_out_values) + '件読み上げます。'
                for i in range(read_out_values):
                    res += str(i + 1) + '番、' + spot_name_list[i] + '。'
                res += '詳細を聞きたい場合は、番号でおっしゃってください。'
                task = 'hear number'
                if len(spot_name_list) == 0:
                    res = '検索結果が0件でした。'
                    task = 'finish'
                
                self.return_state['query_mode'] = 'food'
            elif '観光地' in voice_string:
                spot_name_list, spot_url_list = self.jalan_controller.query_search(self.return_state['where'])
                read_out_values = min(5, len(spot_name_list))
                for i in range(len(spot_name_list)):
                    self.return_state['spot_name_' + str(i)] = spot_name_list[i].replace(' ', '　')
                    self.return_state['spot_url_' + str(i)] = spot_url_list[i]
                self.return_state['previous'] = 'read_kankou'
                self.return_state['read_out_values_first'] = 0
                self.return_state['read_out_values_last'] = read_out_values
                res = 'スポットを' + str(read_out_values) + '件読み上げます。'
                for i in range(read_out_values):
                    res += str(i + 1) + '番、' + spot_name_list[i] + '。'
                res += '詳細を聞きたい場合は、番号でおっしゃってください。'
                task = 'hear number'
                if len(spot_name_list) == 0:
                    res = '検索結果が0件でした。'
                    task = 'finish'
                    
        return res, task
    
    def create_where_detail_res(self, voice_string):
        res = ''
        task = ''
        spot_name_list, spot_url_list = self.jalan_controller.query_search(self.return_state['query'])
        if len(spot_name_list) == 0:
            res = 'すみません。わかりませんでした。'
            task = 'finish'
        else:
            instruction, hours_text, where_text = self.jalan_controller.get_basic_info(spot_url_list[0])
            if instruction != None:
                res = spot_name_list[0] + 'について読み上げます。' + instruction + '。'
            if hours_text != '':
                res += ' ' + hours_text
            elif where_text != '':
                res += '場所は、' + where_text
            if len(res) == 0:
                res = 'すみません。情報がありません。'
            task = 'finish'
        return res, task

    def create_response(self, task_name, rec_str, lat, lng, user_state):
        res = ''
        task = ''
        state = ''
        if task_name == Task.weather:
            where, when, what = self.analyze_whether_text(rec_str)
            where = [where.replace('市', '')]
            if len(where[0]) == 0 and lat != 0 and lng != 0:
                where = []
                data = self.gc_controller.reverse_geo_cording(lat, lng)
                for d in data:
                    if 'locality' in d['types']:
                        where.append(d['short_name'])
                    if 'administrative_area_level_1' in d['types']:
                        where.append(d['short_name'])
            if len(when) == 0:
                res = 'いつの天気ですか？'
                task = 'hear whether when'
                state = 'where=' + str(where)
                return res, task, state
            elif len(where) == 0:
                res = 'どこの天気ですか？'
                task = 'hear whether where'
                state = 'when=' + str(when)
                return res, task, state
            for data in where:
                if len(data) == 0:
                    continue

                res = self.create_weather_res(data, when, what)
                if res == 'where is invalid':
                    res = 'すみません。場所がわかりませんでした。'
            print(where, when, what)
        elif task_name == Task.greeting:
            res = self.create_greeting_res(rec_str)
        elif task_name == Task.news:
            state = 'youtube_url=' + self.create_news_res(rec_str).replace('=', '$equal')
            print(state)
            res = 'わかりました'
            task = 'finish'
        elif task_name == Task.hear_youtube:
            task = 'hear youtube url'
            res = '何を再生しますか？'
        elif task_name == Task.player_stop:
            task = 'stop player'
            res = 'わかりました'
        elif task_name == Task.listen_drive_mode_content:
            where = self.return_state.get('where')
            if where == None or where == '' and lat == 0 and lng == 0:
                task = 'hear drive content where'
                res = 'すみません。場所が取得できませんでした。どこの場所について聞きますか？'
            else:
                task = 'hear drive content'
                res = '何に関して聞きますか？　たべもの、観光地に関してなら答えられます。'
        elif task_name == Task.listen_kankou_where:
            task = 'hear kankou where'
            res = 'どこの観光地について聞きますか？'
        elif task_name == Task.talk_kankou_list:
            res, task = self.create_food_spot_res('hear drive content', rec_str)
        elif task_name == Task.about_hearing:
            res = 'それは観光地ですか？ 食べ物ですか？'
            task = 'hear about hearing mode'
            self.return_state = {}
            node = self.analyze_text(rec_str)
            query = ''
            while node:
                word = node.surface
                if word == 'について':
                    break
                else:
                    hinshi = node.feature.split(",")[0]
                    if hinshi != '助詞':
                        query += word + ','
                node = node.next
            self.set_str2state('query=' + query)
        elif task_name == Task.talk_food_shop:
            where = self.return_state.get('where')
            if self.return_state['food_name'] == '':
                res = '食べ物の名前が取得できませんでした。'
                task = 'finish'
            elif where != None and where != '':
                spot_name_list, spot_url_list = self.jalan_controller.query_search(where + ' ' + self.return_state['food_name'], 'gourmet')
                read_out_values = min(5, len(spot_name_list))
                for i in range(len(spot_name_list)):
                    self.return_state['spot_name_' + str(i)] = spot_name_list[i].replace(' ', '　')
                    self.return_state['spot_url_' + str(i)] = spot_url_list[i]
                self.return_state['previous'] = 'read_kankou'
                self.return_state['read_out_values_first'] = 0
                self.return_state['read_out_values_last'] = read_out_values
                res = 'お店を' + str(read_out_values) + '件読み上げます。'
                for i in range(read_out_values):
                    res += str(i + 1) + '番、' + spot_name_list[i] + '。'
                res += '詳細を聞きたい場合は、番号でおっしゃってください。'
                task = 'hear number'
                if len(spot_name_list) == 0:
                    res = '検索結果が0件でした。'
                    task = 'finish'
            else:
                res = 'どこについて聞きますか？'
                task = 'listen food shop where'
        elif task_name == Task.talk_famous:
            self.get_where_foodname(rec_str)
            where = self.return_state.get('where')
            food_name = self.return_state.get('food_name')
            if food_name != None and food_name != '':
                if where != None and where != '':
                    spot_name_list, spot_url_list = self.jalan_controller.query_search(where + ' ' + food_name, 'gourmet')
                    read_out_values = min(5, len(spot_name_list))
                    for i in range(len(spot_name_list)):
                        self.return_state['spot_name_' + str(i)] = spot_name_list[i].replace(' ', '　')
                        self.return_state['spot_url_' + str(i)] = spot_url_list[i]
                    self.return_state['previous'] = 'read_kankou'
                    self.return_state['read_out_values_first'] = 0
                    self.return_state['read_out_values_last'] = read_out_values
                    res = 'お店を' + str(read_out_values) + '件読み上げます。'
                    for i in range(read_out_values):
                        res += str(i + 1) + '番、' + spot_name_list[i] + '。'
                    res += '詳細を聞きたい場合は、番号でおっしゃってください。'
                    task = 'hear number'
                    if len(spot_name_list) == 0:
                        res = '検索結果が0件でした。'
                        task = 'finish'
                else:
                    res = 'すみません。よくわかりません。'
                    task = 'finish'
            else:
                res = 'すみません。よくわかりません。'
                task = 'finish'

        elif task_name == Task.navigate:
            res = 'すみません。この機能は開発中です。'
            task = 'finish'
        else:
            res = 'すみません。よくわかりません。'
            task = 'finish'

        self.set_str2state(state)
        return res, task
        #return '明日の天気は雨のちくもり、最高気温15度、最低温度9度です。'

    def sound_greeting(self, rec_str):
        if 'おはよう' in rec_str:
            self.system_sound.sound_registered_mp3('good_morning.mp3')
        elif 'こんにちは' in rec_str:
            self.system_sound.sound_registered_mp3('good_afternoon.mp3')
        else:
            self.system_sound.sound_registered_mp3('good_evening.mp3')
    
    def return_result(self, voice_string, data, lat, lng):
        res = ''
        task = ''
        self.set_str2state(data['state'])
        removed_value = self.return_state.pop('youtube_url', None)
        if 'でもない' in voice_string:
            res = 'わかりました'
            task = 'finish'
        elif data['task'] == 'start_listen':
            if self.match_start_str(voice_string):
                res = 'ごようでしょうか'
                task = 'normal hearing'
        elif data['task'] == 'listen food shop where':
            node = self.analyze_text(voice_string)
            where = self.pickup_where(node)
            print(where)
            if where != None:
                self.return_state['where'] = where
                res, task = self.create_response(Task.talk_food_shop, voice_string, lat, lng, data['state'])
            else:
                res = 'すみません。場所がわかりませんでした。'
                task = 'finish'
        elif '他' in voice_string or 'それ以外' in voice_string or '次' in voice_string or 'もっと' in voice_string:
            if self.return_state['previous'] == 'read_kankou':
                spot_name_list = []
                spot_url_list = []
                dict_keys = self.return_state.keys()
                i = 0
                while(True):
                    if 'spot_name_' + str(i) in dict_keys:
                        spot_name_list.append(self.return_state['spot_name_' + str(i)])
                        spot_url_list.append(self.return_state['spot_url_' + str(i)])
                        i += 1
                    else:
                        break
                
                read_out_values_first = int(self.return_state['read_out_values_first'])
                read_out_values_last = int(self.return_state['read_out_values_last'])
                if read_out_values_last == len(spot_name_list):
                    res = 'これ以上ありません。'
                else:
                    next_last = min(read_out_values_last + 5, len(spot_name_list))
                    res = '次の' + str(next_last - read_out_values_last) + '件を読み上げます。'
                    for i in range(read_out_values_last, next_last):
                        res += str(i - read_out_values_last + 1) + '番、' + spot_name_list[i] + '。'
                    self.set_str2state('read_out_values_first=' + str(read_out_values_last))
                    self.set_str2state('read_out_values_last=' + str(next_last))

                    res += '詳細を聞きたい場合は、番号でおっしゃってください。'
                    task = 'hear number'
                task = 'finish'
        elif '番' in voice_string and ('聞きたい' in voice_string or '教えて' in voice_string or 'お願い' in voice_string):
            if self.return_state.get('previous') ==None:
                res = 'すみません。履歴が残っていません。'
                task = 'finish'
            elif self.return_state['previous'] == 'read_kankou':
                spot_name_list = []
                spot_url_list = []
                dict_keys = self.return_state.keys()
                i = 0
                while(True):
                    if 'spot_name_' + str(i) in dict_keys:
                        spot_name_list.append(self.return_state['spot_name_' + str(i)])
                        spot_url_list.append(self.return_state['spot_url_' + str(i)])
                        i += 1
                    else:
                        break
                read_out_values_first = int(self.return_state['read_out_values_first'])
                read_out_values_last = int(self.return_state['read_out_values_last'])
                index = self.kanji2number(voice_string[:voice_string.find('番')])
                index = int(index) - 1 + read_out_values_first
                if index >= len(spot_name_list):
                    res = 'その番号はありません。'
                    task = 'finish'
                else:
                    self.set_str2state('detail_where_name=' + spot_name_list[index])
                    self.set_str2state('detail_where_url=' + spot_url_list[index])
                    instruction, hours_text, where_text = self.jalan_controller.get_basic_info(spot_url_list[index])
                    if instruction != None:
                        res = spot_name_list[index] + 'について読み上げます。' + instruction + '。'
                    if hours_text != '':
                        res += ' ' + hours_text
                    elif where_text != '':
                        res += '場所は、' + where_text
                    if len(res) == 0:
                        res = 'すみません。情報がありません。'
                    task = 'finish'
            elif self.return_state['previous'] == 'read_food':
                spot_name_list = []
                spot_url_list = []
                dict_keys = self.return_state.keys()
                i = 0
                while(True):
                    if 'spot_name_' + str(i) in dict_keys:
                        spot_name_list.append(self.return_state['spot_name_' + str(i)])
                        spot_url_list.append(self.return_state['spot_url_' + str(i)])
                        i += 1
                    else:
                        break
                read_out_values_first = int(self.return_state['read_out_values_first'])
                read_out_values_last = int(self.return_state['read_out_values_last'])
                index = self.kanji2number(voice_string[:voice_string.find('番')])
                index = int(index) - 1 + read_out_values_first
                if index >= len(spot_name_list):
                    res = 'その番号はありません。'
                    task = 'finish'
                else:
                    self.set_str2state('detail_where_name=' + spot_name_list[index])
                    self.set_str2state('detail_where_url=' + spot_url_list[index])
                    instruction = self.jalan_controller.get_specialty_food_basic_info(spot_url_list[index])
                    if instruction != None:
                        res = spot_name_list[index] + 'について読み上げます。' + instruction + '。'
                    if len(res) == 0:
                        res = 'すみません。情報がありません。'
                    task = 'finish'
        elif data['task'] == 'normal' or data['task'] == '':
            task_name = self.classify_tasks(voice_string, data['state']) #聞き取りに対する文章処理
            res, task = self.create_response(task_name, voice_string, lat, lng, data['state'])
        elif data['task'] == 'hear kankou where':
            node = self.analyze_text(voice_string)
            where = self.pickup_where(node)
            res, task = self.create_food_spot_res('hear drive content', where + 'の観光地について教えて')
        elif (data['task'] == 'hear whether where'):
            when = data['state'][5:]
            where = voice_string
            if len(where) != 0:
                where = where.replace('市', '')
            what = ''
            res = self.create_weather_res(where, when, what)
            if res == 'where is invalid':
                res = 'すみません。場所がわかりませんでした。'
            task = 'finish'
        elif (data['task'] == 'hear whether when'):
            where = data['state'][6:]
            if len(where) != 0:
                where = where.replace('市', '')
            when = voice_string
            what = ''
            res = self.create_weather_res(where, when, what)
            if res == 'where is invalid':
                res = 'すみません。場所がわかりませんでした。'
            task = 'finish'
        elif (data['task'] == 'hear youtube url'):
            query = voice_string
            url = self.gc_controller.get_youtube_url(query, order = 'relevance').replace('=', '$equal')
            self.set_str2state('youtube_url=' + url)
            res = 'わかりました。'
            task = 'finish'
        elif data['task'] == 'hear drive content':
            res, task = self.create_food_spot_res(data['task'], voice_string)
        elif data['task'] == 'hear about hearing mode':
            if '観光地' in voice_string:
                res, task = self.create_where_detail_res(voice_string)
            else:
                res = 'すみません。場所がよくわかりませんでした。'
                task = 'finish'
        elif data['task'] == 'hear drive content where':
            node = self.analyze_text(voice_string)
            where = self.pickup_where(node)
            if len(where) != 0:
                self.return_state['where'] = where
                task = 'hear drive content'
                res = '何に関して聞きますか？　たべもの、観光地に関してなら答えられます。'
            else:
                task = 'finish'
                res = 'すみません。場所がわかりませんでした。'
        state = self.get_state()
        
        print(res)
        print(task)
        print(state)
        
        return res, task, state

    def main_loop(self):
        while(True):
            self.recognize_call('Z') #起動聞き取り
            print('success')
            self.system_sound.sound_registered_mp3('start.mp3') #聞き取り音再生
            time.sleep(0.1)
            self.system_sound.sound_registered_mp3('start_record.mp3') #聞き取り開始音再生
            time.sleep(0.5)
            rec_str = self.recording(record_seconds=2,filtering = False, mode = 'google') #内容聞き取り
            print(rec_str)
            task_name = self.classify_tasks(rec_str) #聞き取りに対する文章処理
            if task_name == Task.default:
                self.system_sound.sound_registered_mp3('default.mp3')
            elif task_name == Task.greeting:
                self.sound_greeting(rec_str)
            else:
                res, task = self.create_response(task_name, rec_str) #返答生成
                file_name = self.system_sound.create_sound(res)
                self.system_sound.sound_dev_mp3(file_name)
            time.sleep(0.5)

if __name__ == "__main__":
    main = Main()
    self.main_loop()
    #sound = record_sound()
    #record_sound.start_record()