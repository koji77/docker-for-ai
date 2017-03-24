# termextract: Termextract検証環境
* TermExtract: 専門用語(キーワード)を自動抽出するPerlモジュール
* URL: <http://gensen.dl.itc.u-tokyo.ac.jp/termextract.html>

## コンテナの構成
| 項目        | バージョン | 備考 |
|:-----------|:------------|:------------|
| CentOS     | 7 | ja_JP.UTF-8|
| perl | 5.16.3 | yum base |
| MeCab     | 0.996 | --enable-utf8-only|
| MeCab IPAdic | 2.7.0-20070801 |--with-charset=utf8|
| MeCab IPAdic model | 2.7.0-20070801 ||
| MeCab perl | 0.996 ||
| TermExtract | 4_10 ||

## 事前作業
*  ホストマシンにエイリアスを登録する。
``` bash
echo alias termextract-bash=\"nvidia-docker run --rm -v /root/docker-for-ai/termextract/data:/var/lib/termextract -a stdin -a stdout -a stderr -i 29koji/termextract /bin/bash\" >> ~/.bashrc
echo alias termextract=\"nvidia-docker run --rm -v /root/docker-for-ai/termextract/data:/var/lib/termextract -a stdin -a stdout -a stderr -i 29koji/termextract termextract_mecab.pl\" >> ~/.bashrc
echo alias mecab-ipa=\"nvidia-docker run --rm -v /root/docker-for-ai/termextract/data:/var/lib/termextract -a stdin -a stdout -a stderr -i 29koji/termextract mecab\" >> ~/.bashrc
source ~/.bashrc
```

## Dockerイメージ作成
``` bash
cd /root/docker-for-ai/termextract
nvidia-docker build -t 29koji/termextract .
```

## 使い方
``` bash
# echoまたはcatのテキスト出力とパイプで結合する。
# 入力形式はUTF8の文字コードのテキストのみ
# 1:専門用語+重要度、2:専門用語のみ、3:カンマ区切り、4:IPAdic辞書形式(コスト推定)、5:IPAdic辞書形式(文字列長)
echo "印刷用紙を複合機で印刷する。" | termextract
echo "印刷用紙を複合機で印刷する。" | termextract --output 4
```
### 自動コスト推定した辞書の追加
``` bash
termextract-bash
echo "印刷用紙を複合機で印刷する。" | termextract_mecab.pl --output 4 > /mecab-ipadic-2.7.0-20070801/user.csv
cd /mecab-ipadic-2.7.0-20070801
nkf -e --overwrite user.csv
make clean
./configure --with-charset=utf8
make
make install
echo "印刷用紙を複合機で印刷する。" | mecab
exit
```

### 文字列長に応じた低コスト辞書の追加
``` bash
termextract-bash
echo "印刷用紙を複合機で印刷する。" | termextract_mecab.pl --output 5 > /mecab-ipadic-2.7.0-20070801/user.csv
cd /mecab-ipadic-2.7.0-20070801
nkf -e --overwrite user.csv
make clean
./configure --with-charset=utf8
make
make install
echo "印刷用紙を複合機で印刷する。" | mecab
exit
```
