import subprocess
import tempfile
import os

class PyJtalk():
    def __init__(self,hts_voice='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'):
        self.hts_voice=hts_voice
        self.dic='/var/lib/mecab/dic/open-jtalk/naist-jdic'
        self.openjtalk_bin = 'open_jtalk'

    def say(self,msg:str,**args):
        try:
            temp = tempfile.mkdtemp()
            text = os.path.join(temp,'text.txt')
            voice = os.path.join(temp,'voice.wav')
            with open(text,'w') as f:
                f.write(msg)

            ops = " ".join(['-'+str(x)+' '+str(args[x]) for x in args])
            subprocess.run('%s %s -m %s -x %s -ow %s %s'%(self.openjtalk_bin,ops,self.hts_voice,self.dic,voice,text),shell=True,check=True)
            subprocess.run('aplay %s'%(voice),shell=True,check=True)
        finally:
            os.remove(text)
            os.remove(voice)
            
    def synthesize(self,msg:str,out:str,**args):
        try:
            temp = tempfile.mkdtemp()
            text = os.path.join(temp,'text.txt')
            voice = out
            with open(text,'w') as f:
                f.write(msg)

            ops = " ".join(['-'+str(x)+' '+str(args[x]) for x in args])
            subprocess.run('%s %s -m %s -x %s -ow %s %s'%(self.openjtalk_bin,ops,self.hts_voice,self.dic,voice,text),shell=True,check=True)
            
        finally:
            os.remove(text)
        

if __name__=="__main__":
    p = PyJtalk()
    p.say("こんにちは",r=0.6)
