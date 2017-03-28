# ruby-dev: Ruby開発環境

## コンテナの構成
* OS: CentOS7
* Ruby: 2.4.0
* rbenv: https://github.com/sstephenson/rbenv.git

## Dockerイメージ作成
``` bash
nvidia-docker build -t 29koji/ruby-dev .
```

# Wikipedia日本語版コーパスの作成〜学習済モデル作成・配置
``` bash
# Dockerコンテナ作成 & 実行(Dockerfileの設定により、/bin/bashが起動する。)
nvidia-docker run --rm -v /root/docker-for-ai/ruby-dev/data:/var/lib/rubydev -it 29koji/ruby-dev

# Wikipedia日本語ページののDumpデータをダウンロード
# jawiki-latest-pages-articles.xml.bz2のサイズ: 約2.46GB(2,462,875,139)
wget -P /var/lib/rubydev https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

# wikipediaのDumpデータをテキストファイルに変換(2h07m)
# 551個のファイルが生成される。(それぞれ10MB程度)
cd /var/lib/rubydev
time wp2txt --input-file jawiki-latest-pages-articles.xml.bz2

# 不要な文字削除とNFKC正規化(ひらがな、かたかな → 全角 数字、英字 → 半角 記号文字の正規化(例: ⑧ → 8)
time python datasetup.py jawiki-latest-pages-articles.xml-*.txt

# 一つのファイルにまとめる。
# jawiki.txtのサイズ: 約5.04GB(5,038,197,217) 処理時間: 約24秒
time cat jawiki-latest-pages-articles.xml-*.txt_cleanuped.txt > jawiki.txt

# 中間ファイル削除
rm -f jawiki-latest-pages-articles.xml-*.txt_cleanuped.txt
rm -f jawiki-latest-pages-articles.xml-*.txt
rm -f jawiki-latest-pages-articles.xml.bz2

exit

# 分かちを入れる。
# jawiki_wakati.txtのサイズ: 約5.70GB(5,698,253,200 処理時間: 約52分
mv /root/docker-for-ai/ruby-dev/data/jawiki.txt /root/docker-for-ai/word2vec/data/.
word2vec-bash
# mecabのオプション(-b)でinput bufferを拡張しないとエラー(input-buffer overflow. The line is split. use -b #SIZE option.)となる。最大値は、8,192x640=5,242,880
time cat /var/lib/word2vec/jawiki.txt | mecab -b 5242880 -Owakati > /var/lib/word2vec/jawiki_wakati.txt
exit

# word2vecに学習させる。
# 単語数: 約8億語(804,754,377)
# jawiki.binのサイズ: 約1.42GB(1,420,814,840) 処理時間: 約45分
time word2vec -train /var/lib/word2vec/jawiki_wakati.txt -output /var/lib/word2vec/jawiki.bin -size 200 -window 5 -negative 5 -hs 0 -sample 1e-3 -threads 8 -binary 1

# 中間ファイル削除
rm -f /root/docker-for-ai/word2vec/data/jawiki_wakati.txt
rm -f /root/docker-for-ai/word2vec/data/jawiki.txt
```
