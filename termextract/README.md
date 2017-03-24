# termextract: Termextract検証環境
* TermExtract: 専門用語(キーワード)を自動抽出するPerlモジュール
  * 基本的に名詞が連続したら複合語として扱う。
  * 統計的に分かっている単名詞同士の結びつきで重要度を判定
  * 入力テキストにおける複合語の出現回数を掛けることで重要度を更新することも可能
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
echo alias termextract-bash=\"nvidia-docker run --rm -v /root/docker-for-ai/termextract/data:/var/lib/termextract -a stdin -a stdout -a stderr -it 29koji/termextract /bin/bash\" >> ~/.bashrc
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

### MeCabのIPAdicでの解析結果
``` bash
echo "印刷用紙を複合機で印刷する。" | mecab-ipa
印刷    名詞,サ変接続,*,*,*,*,印刷,インサツ,インサツ
用紙    名詞,一般,*,*,*,*,用紙,ヨウシ,ヨーシ
を      助詞,格助詞,一般,*,*,*,を,ヲ,ヲ
複合    名詞,サ変接続,*,*,*,*,複合,フクゴウ,フクゴー
機      名詞,接尾,一般,*,*,*,機,キ,キ
で      助詞,格助詞,一般,*,*,*,で,デ,デ
印刷    名詞,サ変接続,*,*,*,*,印刷,インサツ,インサツ
する    動詞,自立,*,*,サ変・スル,基本形,する,スル,スル
。      記号,句点,*,*,*,*,。,。,。
EOS
```

### TermExtractによる専門用語(キーワード)自動抽出結果
``` bash
# echoまたはcatのテキスト出力とパイプで結合する。
# 入力形式はUTF8の文字コードのテキストのみ
# 1:専門用語+重要度、2:専門用語のみ、3:カンマ区切り、4:IPAdic辞書形式(コスト推定)、5:IPAdic辞書形式(文字列長)
echo "印刷用紙を複合機で印刷する。" | termextract
複合機   1.41
印刷用紙 1.41

echo "印刷用紙を複合機で印刷する。" | termextract --output 4
複合機,1285,1285,7336,名詞,一般,*,*,*,*,複合機,*,*,ByTermExtractEst
印刷用紙,1285,1285,7336,名詞,一般,*,*,*,*,印刷用紙,*,*,ByTermExtractEst
```

### 自動コスト推定した辞書の追加
* MeCabで自動コスト推定した結果を辞書に追加
* 自動コスト推定のアルゴリズムに関するコード以外の公開情報が見つからなかった。

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
印刷用紙	名詞,一般,*,*,*,*,印刷用紙,*,*,ByTermExtractEst
を	助詞,格助詞,一般,*,*,*,を,ヲ,ヲ
複合	名詞,サ変接続,*,*,*,*,複合,フクゴウ,フクゴー
機	名詞,接尾,一般,*,*,*,機,キ,キ
で	助詞,格助詞,一般,*,*,*,で,デ,デ
印刷	名詞,サ変接続,*,*,*,*,印刷,インサツ,インサツ
する	動詞,自立,*,*,サ変・スル,基本形,する,スル,スル
。	記号,句点,*,*,*,*,。,。,。
EOS
exit
```

### 文字列長に応じた低コスト辞書の追加
* 長い用語(複合語の可能性が高い)のコストを極端に低くすることで専門用語が優先的に切りだされるようにする。
* この方法はすでに存在する用語を押しのけて切り出されるようにするため、短い用語や一般的な用語を除外する必要がある。

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
印刷用紙	名詞,一般,*,*,*,*,印刷用紙,*,*,ByTermExtractLen
を	助詞,格助詞,一般,*,*,*,を,ヲ,ヲ
複合機	名詞,一般,*,*,*,*,複合機,*,*,ByTermExtractLen
で	接続詞,*,*,*,*,*,で,デ,デ
印刷	名詞,サ変接続,*,*,*,*,印刷,インサツ,インサツ
する	動詞,自立,*,*,サ変・スル,基本形,する,スル,スル
。	記号,句点,*,*,*,*,。,。,。
EOS
exit
```
