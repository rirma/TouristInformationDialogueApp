#!/bin/sh
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR
wget -O hts_engine.tar.gz https://sourceforge.net/projects/hts-engine/files/hts_engine%20API/hts_engine_API-1.10/hts_engine_API-1.10.tar.gz/download
tar xvf hts_engine.tar.gz
rm -rf hts_engine.tar.gz
hts_engine=`ls -t|grep hts_engine|head -n 1`
cd $hts_engine
./configure
make
cd ..
wget -O open_jtalk.tar.gz https://sourceforge.net/projects/open-jtalk/files/Open%20JTalk/open_jtalk-1.10/open_jtalk-1.10.tar.gz/download
tar xvf open_jtalk.tar.gz
rm -rf open_jtalk.tar.gz
jtalk=`ls -t|grep open_jtalk|head -n 1`
cd $jtalk
./configure  --with-hts-engine-header-path=$SCRIPT_DIR/$hts_engine/include --with-hts-engine-library-path=$SCRIPT_DIR/$hts_engine/lib --with-charset=utf-8
make
cd ..
wget -O open_jtalk_dic_utf_8.tar.gz https://sourceforge.net/projects/open-jtalk/files/Dictionary/open_jtalk_dic-1.10/open_jtalk_dic_utf_8-1.10.tar.gz/download
tar xvf open_jtalk_dic_utf_8
rm -rf open_jtalk_dic_utf_8.tar.gz
dic=`ls -t|grep open_jtalk_dic|head -n 1`
wget -O hts_voice_nitech_jp_atr503_m001.tar.gz https://sourceforge.net/projects/open-jtalk/files/HTS%20voice/hts_voice_nitech_jp_atr503_m001-1.05/hts_voice_nitech_jp_atr503_m001-1.05.tar.gz/download
tar xvf hts_voice_nitech_jp_atr503_m001.tar.gz
rm -rf hts_voice_nitech_jp_atr503_m001.tar.gz
hts_voice=`ls -t|grep hts_voice_nitech|head -n 1`
