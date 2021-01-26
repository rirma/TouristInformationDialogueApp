import requests
from bs4 import BeautifulSoup
import csv

#じゃらんのサイトからスクレイピングするためのクラス
class jalan_controller():
    def __init__(self):
        self.where_data = []
        self.where_child_data = []
        self.where_child_detail_data = []
        with open('../dev/jalan_data/data.csv') as f:
            reader = csv.reader(f)
            self.where_data = [row for row in reader]
        with open('../dev/jalan_data/child_data.csv') as f:
            reader = csv.reader(f)
            self.where_child_data = [row for row in reader]
        with open('../dev/jalan_data/child_detail_data.csv') as f:
            reader = csv.reader(f)
            self.where_child_detail_data = [row for row in reader]
    
    def get_specialty_food(self, where, parent_where, where_type=''):
        print(where)
        print(parent_where)
        url = ''
        result_where = ''
        if where_type == 'prefectures':
            for i in range(len(self.where_data)):
                if where in self.where_data[i][1]:
                    url = 'https://www.jalan.net/gourmet/' + self.where_data[i][0] + '/menu/'
                    result_where = where
                    break
        else:
            for i in range(len(self.where_child_detail_data)):
                if where in self.where_child_detail_data[i][2]:
                    url = 'https://' + self.where_child_detail_data[i][1] + 'menu/'
                    result_where = where
                    break
            if url == '':
                for i in range(len(self.where_data)):
                    if where in self.where_child_data[i][2]:
                        url = 'https://' + self.where_child_data[i][1] + 'menu/'
                        result_where = where
                        break
            if url == '':
                for i in range(len(self.where_data)):
                    if parent_where in self.where_data[i][1]:
                        url = 'https://www.jalan.net/gourmet/' + self.where_data[i][0] + '/menu/'
                        result_where = where
                        break
        if url == '':
            return '', '', ''
        print(url)
        
        site = requests.get(url)
        site.encoding = site.apparent_encoding
        spot_content = BeautifulSoup(site.text, 'html.parser')

        spot_list = spot_content.find_all('div', class_='item-listContents')

        spot_name_list = []
        spot_url_list = []
        for data in spot_list:
            spot_name = data.find('p', class_='item-name').find('a').text.replace('\u3000', ' ')
            spot_name_list.append(spot_name)

            spot_url = 'https://www.jalan.net' + data.find('p', class_='item-name').find('a').get('href')
            spot_url_list.append(spot_url)

        return where, spot_name_list, spot_url_list

    def get_specialty_food_basic_info(self, url):
        site = requests.get(url)
        site.encoding = site.apparent_encoding
        html_data = BeautifulSoup(site.text, 'html.parser')
        instruction = html_data.find(id='aboutArea')
        if instruction != None:
            instruction = instruction.find('p').text

        return instruction
        
    def query_search(self, query, mode='kankou'):
        query = query.replace(',', ' ')
        result = 'https://www.jalan.net/' + mode + '/kw_'
        query = query.encode('shift_jis')
        for data in query:
            data_string = format(data, 'x')
            result += '%25' + data_string
        result += '/'
        site = requests.get(result)
        site.encoding = site.apparent_encoding
        html_data = BeautifulSoup(site.text, 'html.parser')
        spot_content = html_data.find(id='cassetteType')
        spot_list = spot_content.find_all('div', class_='item-listContents')
        
        spot_name_list = []
        spot_url_list = []
        for data in spot_list:
            spot_name = data.find('p', class_='item-name').find('a').text.replace('\u3000', ' ')
            spot_name_list.append(spot_name)

            spot_url = 'https://www.jalan.net' + data.find('p', class_='item-name').find('a').get('href')
            spot_url_list.append(spot_url)

        return spot_name_list, spot_url_list
    
    def get_basic_info(self, url):
        site = requests.get(url)
        site.encoding = site.apparent_encoding
        html_data = BeautifulSoup(site.text, 'html.parser')
        instruction = html_data.find(id='aboutArea')
        if instruction != None:
            instruction = instruction.find('p').text
        
        hours = html_data.find('table', class_='basicInfoTable')
        hours_text = ''
        where_text = ''
        td_list = hours.find_all('td')
        for data in td_list:
            text = data.text.replace('\t', '').replace('\n', '').replace('※', '')
            if '時間' in text or '営業' in text:
                hours_text = text
            elif '〒' in text:
                address = text.split(' ')
                if len(address) > 2:
                    where_text = address[1].replace('MAP', '')
                else:
                    address = text.split('　')
                if len(address) > 2:
                    where_text = address[1].replace('MAP', '')
                else:
                    where_text = text
        #hours_text = hours.find('td').text.replace('\t', '').replace('\n', '').replace('※', '')

        return instruction, hours_text, where_text