# TouristInformationDialogueApp
観光案内をするためのアプリ  
This is an app to help you with sightseeing.

日本語のみ対応しています。  
Only Japanese is supported.

# 実行環境
Unity version 2019.3.13f1 以上  
docker version 19.03.12 以上 (他バージョン未確認)  
compose version 1.27.2 以上 (他バージョン未確認)  
  
上記環境があれば、windowsでもubuntuでも動作します。  

# 使い方
## フロント側セットアップ(Unity)
・下記URLより、Z-Free-Assets.unitypackageをダウンロード  
[Unity Package](https://drive.google.com/drive/folders/1AreXpIHI56P5RTgqWewJQouHp3pc3oO3?usp=sharing)  
  
・Unityより、Z-Free-Assets.unitypackageをインポート  
(Assets -> import package -> custom packageよりインポート)
  
・Unityインスペクタより、Assets -> original -> Scenes -> ForMacを選択し、シーン読み込み  
(windowsでも問題ありません)

## バック側セットアップ(python flaskサーバ)
ターミナルより、ubuntu18.04に移動  
以下コマンドにより、docker立ち上げ & 仮想環境内に入る  
(※開発中のため、50GBくらいの容量を必要とします。また、立ち上げにものすごく時間がかかります。)

```bash
docker-compose up -d --build
docker-compose exec z_server bash
```

仮想環境内で、以下コマンドによりフォルダ移動

```bash
cd /root/opt/public/src/
```
### 音声認識に「julius」を使う場合
juliusは音声認識精度は悪いが、仮想環境構築時に既にダウンロードされるようにしているため、すぐにこのアプリを実施できる。　　
  
以下コマンドによりローカル環境にサーバを立ち上げ
```bash
bash run_julius_server.sh
```

### 音声認識に「Cloud Speech-to-Text API」を使う場合
音声認識精度は良いが、APIキーを取得するまでが手続きがめんどくさい。  
また、使いすぎると料金が発生するので、注意が必要である。  
  
手順1 google clooud platformより、「Cloud Speech-to-Text API」のAPIを取得し、認証情報が記述されたjsonファイルをダウンロードする。  
[APIキー取得参考url](https://qiita.com/knyrc/items/7aab521edfc9bfb06625)  
  
手順2 ダウンロードしたjsonファイルを、下記フォルダ内に保存する
```bash
ubuntu18.04/opt/public/Auth/
```

手順3 以下フォルダパスにあるファイルを編集する。
```bash
ubuntu18.04/opt/public/src/main.py
```

[]で囲まれている部分に、取得したファイル名やAPIキーを入力してください。
```bash
self.gc_controller = GoogleCloudController('../Auth/[保存したファイル名]', api_key = '[Cloud Speech-to-Text APIのキー]')
self.forecast = Forecast('[open weather map APIのキー]')
```

天気予測もしたい場合、open weather mapのapiを取得し、[open weather map apiのキー]に記述してください。(無くても問題ないです。)  
  
手順4 以下コマンドによりローカル環境にサーバを立ち上げ
```bash
bash run_google_server.sh
```

## unity実行
フロント側、バックエンド側のセットが終われば、あとはUnityを実行するだけです。

# 対話シナリオ例
このアプリでは、観光案内や名物を聞くことができます。「Z(ゼット)」と呼びかけると起動します。  
また、このアプリでは、「フォンッ」という音と、「ピロンッ」という音の2種類を使い分けており、ユーザはこの音が鳴った後に話しかけることができるようになります。  
「フォンッ」という音が鳴った場合、アプリとユーザとのインタラクションが終了するため、再びアプリに話しかけたければ、「Z(ゼット)」と呼びかけ直す必要があります。  
「ピロンッ」という音は、対話継続を意味し、アプリに問いかけられたことに対して回答すれば、再び何かを返してくれます。  
対話を終了したい場合、「何でもない」と言えば対話終了となります。

## 対話例
### 例1 観光地を聞く
ユーザ: ゼット！  
アプリ: 御用でしょうか。(ピロンッ)  
ユーザ: 東京で有名な観光地は？  
アプリ: 東京で有名な観光地を5件読み上げます。1番・・・、2番・・・、・・・詳細を聞きたい場合は番号でおっしゃってください。(ピロンッ)  
ユーザ: 1番教えて！  
アプリ: ・・・について読み上げます。・・・(フォンッ)  

### 例2 名物・食べ物を聞く
ユーザ: ゼット！  
アプリ: 御用でしょうか。(ピロンッ)  
ユーザ: 札幌の名物は？(東京でおいしい食べ物は？)    
アプリ: 札幌の名物を5件読み上げます。1番・・・、2番・・・、・・・詳細を聞きたい場合は番号でおっしゃってください。(ピロンッ)  
ユーザ: 1番教えて！  
アプリ: ・・・について読み上げます。・・・(フォンッ)  

### 例3 食べ物で有名な場所を聞く
ユーザ: ゼット！  
アプリ: 御用でしょうか。(ピロンッ)  
ユーザ: ラーメン食べたい。   
アプリ: 札幌の名物を5件読み上げます。1番・・・、2番・・・、・・・詳細を聞きたい場合は番号でおっしゃってください。(ピロンッ)  
ユーザ: 1番教えて！  
アプリ: ・・・について読み上げます。・・・(フォンッ)  

# 音声ファイルについて
このアプリでは、解析を目的としてバックエンド側に音声を保存しています。容量がいっぱいになった時は、以下のフォルダに保存されている音声ファイルを削除してください。

```bash
/root/opt/public/sound/original/
/root/opt/public/sound/system_sound/dev/
```

# 注意事項
このアプリは、勉強や研究等を目的として開発しており、観光情報は[じゃらん](https://www.jalan.net)から取得しています。  
もしこのアプリを「勉強・研究」の域を超えて使うことで不利益が生じた場合、私は一切の責任を負いかねます。