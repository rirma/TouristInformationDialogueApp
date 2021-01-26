
FROM debian as builder
ENV JUMAN_VERSION 2.0.0-rc3
ENV JUMAN_DIR jumanpp-${JUMAN_VERSION}
ENV JUMAN_URL https://github.com/ku-nlp/jumanpp/releases/download/v${JUMAN_VERSION}/jumanpp-${JUMAN_VERSION}.tar.xz
ENV KNP_VERSION 4.20
ENV KNP_DIR knp-${KNP_VERSION}
ENV KNP_URL http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/${KNP_DIR}.tar.bz2
RUN apt update && \
    apt -y upgrade && \
    apt install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    cmake \
    xz-utils \
    bzip2 \
    libz-dev \
    wget && \
    echo "${JUMAN_URL}" && \
    wget -q --no-check-certificate ${JUMAN_URL} -O ${JUMAN_DIR}.tar.xz && \
    tar -Jxvf ${JUMAN_DIR}.tar.xz && \
    rm ${JUMAN_DIR}.tar.xz && \
    cd ${JUMAN_DIR} && \
    mkdir bld && \
    cd bld && \
    cmake .. \
    -DCMAKE_BUILD_TYPE=Release && \
    make install -j 4 && \
    cd ../.. && \
    echo "jumanpp install done" && \
    echo "${KNP_URL}" && \
    wget -q --no-check-certificate ${KNP_URL} -O ${KNP_DIR}.tar.bz2 && \
    tar jxvf ${KNP_DIR}.tar.bz2 && \
    rm ${KNP_DIR}.tar.bz2 && \
    cd ${KNP_DIR} && \
    ./configure && \
    make && \
    make install && \
    echo "KNP install done"

FROM ubuntu:18.04 as runner
COPY --from=builder /usr/local /usr/local
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y sudo && \
    apt-get install -y vim && \
    apt-get install -y pulseaudio && \
    apt-get install -y build-essential curl file git && \
    useradd -m -s /bin/zsh linuxbrew && \
    usermod -aG sudo linuxbrew &&  \
    mkdir -p /home/linuxbrew/.linuxbrew && \
    chown -R linuxbrew: /home/linuxbrew/.linuxbrew
USER linuxbrew
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
USER root
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"

RUN brew install portaudio && \
    apt-get install -y python3 python-dev python3-dev \
    build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    python-pip python3-pip && \
    apt-get --assume-yes install libasound-dev portaudio19-dev     libportaudio2 libportaudiocpp0 && \
    pip3 install --upgrade setuptools && \
    pip3 install gtts && \
    pip3 install pyaudio && \
    pip3 install pygame mutagen && \
    pip3 install numpy && \
    pip3 install SpeechRecognition

WORKDIR /data
RUN pwd
RUN apt-get install wget && \
    wget https://github.com/julius-speech/julius/archive/v4.4.2.tar.gz && \
    tar zxvf v4.4.2.tar.gz
WORKDIR /data/julius-4.4.2
RUN pwd
RUN ./configure && \
    make && \
    make install

RUN apt-get install unzip
WORKDIR /data/julius-4.4.2/julius-kit
RUN wget https://github.com/julius-speech/grammar-kit/archive/v4.3.1.zip && \
    wget https://osdn.net/projects/julius/downloads/66544/dictation-kit-v4.4.zip && \
    unzip v4.3.1.zip && \
    unzip dictation-kit-v4.4.zip && \
    pip3 install matplotlib && \
    pip3 install scipy && \
    pip3 install pytz && \
    pip3 install geoip2 && \
    pip3 install tqdm && \
    pip3 install bs4 && \
    pip3 install lxml && \
    pip3 install google-cloud-speech==1.1.0 && \
    pip3 install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api && \
    apt install net-tools && \
    pip3 install flask && \
    pip3 install flask_socketio && \
    pip3 install flask_cors && \
    pip3 install pydub && \
    apt-get install -y ffmpeg && \
    apt-get install -y frei0r-plugins && \
    pip3 install waitress && \
    pip3 install translate && \
    echo yes | brew install mecab && \
    echo yes | brew install mecab-ipadic && \
    pip3 install mecab-python3 && \
    pip3 install unidic-lite && \
    pip3 install google-api-python-client && \
    pip3 install pyknp && \
    pip3 install jaconv

WORKDIR /root
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /root/mecab-ipadic-neologd/
RUN echo yes | ./bin/install-mecab-ipadic-neologd -n
