# pyjtalk
OpenJtalk Python Wrapper

# install
```sh
sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk
pip install pyjtalk
```

# usage
```py
from pyjtalk.pyjtalk import PyJtalk()
p = PyJtalk()
p.say("こんにちは")
```
