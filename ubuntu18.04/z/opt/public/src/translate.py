from googletrans import Translator
import sys

class Translate():
    def trans(self, line, src = 'en', dest = 'ja', try_num = 10):
        translator = Translator(service_urls=['translate.googleapis.com'])
        translated = None
        for _ in range(try_num):
            try:
                translated = translator.translate(line, src=src, dest=dest)
                break
            except Exception as e:
                translator = Translator(service_urls=['translate.googleapis.com'])
        return translated

if __name__ == "__main__":
    trans = Translate()
    print(trans.trans("It will cloudy tomorrow.").text)
