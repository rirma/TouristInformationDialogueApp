from pyknp import Juman
import sys

jumanpp = Juman()

# return list [[見出し, 読み, 原形, 品詞, 品詞細分類, 活用型, 活用形, 意味情報, 代表表記]]
def analyze_text_by_juman(text):
    result = jumanpp.analysis(text)
    result_list = []
    for mrph in result.mrph_list(): # 各形態素にアクセス
        result_list.append([mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname])
    return result_list

if __name__ == '__main__':
    args = sys.argv
    result_text = analyze_text_by_juman(args[1])
    for text in result_text:
        print(','.join(text))