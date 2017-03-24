# word2vec: Word2Vec検証環境

## コンテナの構成
| 項目        | バージョン | 備考 |
|:-----------|:------------|:------------|
| CentOS     | 7 | ja_JP.UTF-8|
| MeCab     | 0.996 | --enable-utf8-only|
| MeCab IPAdic | 2.7.0-20070801 |--with-charset=utf8|
| GCC | 4.8.2-16 ||
| word2vec | https://github.com/svn2github/word2vec.git | |
| ICU | 50.1.2-11 ||
| RE2 | 20130115-2 ||
| WordNet | 3.0-21 ||
| glib2 | 2.36.3-5 ||
| gflags | 1.3-7 ||
| word2vec-calc |https://github.com/naoa/word2vec-calc|word2vecの学習済モデルを使用してベクトルの加減算ができるプログラム|

## 事前作業
*  ホストマシンにエイリアスを登録する。
``` bash
echo alias word2vec-bash=\"nvidia-docker run --rm -v /root/docker-for-ai/word2vec/data:/var/lib/word2vec -a stdin -a stdout -a stderr -it 29koji/word2vec /bin/bash\" >> ~/.bashrc
echo alias word2vec=\"nvidia-docker run --rm -v /root/docker-for-ai/word2vec/data:/var/lib/word2vec -a stdin -a stdout -a stderr -i 29koji/word2vec word2vec\" >> ~/.bashrc
echo alias word2vec-distance=\"nvidia-docker run --rm -v /root/docker-for-ai/word2vec/data:/var/lib/word2vec -a stdin -a stdout -a stderr -it 29koji/word2vec distance /var/lib/word2vec/jawiki.bin\" >> ~/.bashrc
echo alias word2vec-calc=\"nvidia-docker run --rm -v /root/docker-for-ai/word2vec/data:/var/lib/word2vec -a stdin -a stdout -a stderr -i 29koji/word2vec word2vec-calc\" >> ~/.bashrc
echo alias mecab-NEologd=\"nvidia-docker run --rm -v /root/docker-for-ai/word2vec/data:/var/lib/word2vec -a stdin -a stdout -a stderr -i 29koji/word2vec mecab\" >> ~/.bashrc
source ~/.bashrc
```

* MeCab新語辞書: mecab-ipadic-NEologdの配置
  * あらかじめmecabを使用して「mecab-user-dict-seed-20170213.dic」を作成しておく。
  * 作成した辞書を「/root/docker-for-ai/word2vec」配下に配置する。

* Wikipedia日本語版コーパスから作成した学習済モデルの配置
  * あらかじめ学習済モデル「jwiki.bin」を作成しておく。
  * 作成した辞書を「/root/docker-for-ai/word2vec/data」配下に配置する。

## Dockerイメージ作成
``` bash
cd /root/docker-for-ai/word2vec
nvidia-docker build -t 29koji/word2vec .
```

## 使い方
``` bash
# コサイン距離計算
# 日本語の計算は、macかLinuxで実施
word2vec-distance
# Enter word or sentence (EXIT to break): 首相

# 加減算
# 男 → 王様の関係を女に適用したものは何か？(期待値: 女王)
echo "王様 - 男 + 女" | word2vec-calc --file_path /var/lib/word2vec/jawiki.bin --output 1
# フランス → パリの関係を日本に適用したものは何か？(期待値: 東京)
echo "パリ - フランス + 日本" | word2vec-calc --file_path /var/lib/word2vec/jawiki.bin --output 1

# グラフ出力
word2vec-bash
cd /var/lib/word2vec/mycorpus
python vis.py
# query: 曹操, 司馬懿, 荀彧, 劉備, 諸葛亮, 関羽, 張飛
exit
mv /root/docker-for-ai/word2vec/data/scatter-*.png /home/ubuntu/.

# <参考>word2vec可視化環境構築下準備
word2vec-bash
cd /var/lib/word2vec
wget -P /tmp https://github.com/nishio/word2vec_boostpython/archive/master.zip
unzip /tmp/master.zip
mv word2vec_boostpython-master word2vec_boostpython
cd word2vec_boostpython
# vi setup.py

cd /var/lib/word2vec
wget -P /tmp https://github.com/nishio/mycorpus/archive/master.zip
unzip /tmp/master.zip.1
mv mycorpus-master mycorpus
cd mycorpus
# vi vis.py

exit
```

## <参考>MeCab新語辞書: mecab-ipadic-NEologdの作成方法

``` bash
# mecab環境へログイン
word2vec-bash

# 辞書データ取得
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git

# 辞書データの元となるCSVを解凍する。
xz -dkv mecab-ipadic-neologd/seed/mecab-user-dict-seed.*.csv.xz

# csvから辞書ファイル作成
/usr/local/libexec/mecab/mecab-dict-index -d /usr/local/lib/mecab/dic/ipadic -u /usr/local/lib/mecab/dic/mecab-user-dict-seed-20170213.dic -f utf-8 -t utf-8 /mecab-ipadic-neologd/seed/mecab-user-dict-seed.20170213.csv

# 辞書ファイル登録
echo "userdic = /usr/local/lib/mecab/dic/mecab-user-dict-seed-20170213.dic" >> /usr/local/etc/mecabrc
```
