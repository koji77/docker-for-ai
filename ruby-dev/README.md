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
nvidia-docker run --rm -v /root/docker-for-ai/ruby-dev/data:/var/lib/rubydev -it 29koji/ruby-dev

# Wikipedia日本語ページののXMLデータをダウンロード
# jawiki-latest-pages-articles.xml.bz2のサイズ: 約2.46GB(2,462,875,139)
wget -P /var/lib/rubydev https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

# wikipediaのデータ(XML)をテキストファイルに変換(2h07m)
# 551個のファイルが生成される。(それぞれ10MB程度)
cd /var/lib/rubydev
time wp2txt --input-file jawiki-latest-pages-articles.xml.bz2

# 不要な文字を削除
time python datasetup.py jawiki-latest-pages-articles.xml-*.txt

# 一つのファイルにまとめる。
# jawiki_wakati.txtのサイズ: 約5.45GB(5,452,825,410) 処理時間: 約50秒
time cat jawiki-latest-pages-articles.xml-*.txt_cleanuped.txt > jawiki.txt

# 中間ファイル削除
rm -f jawiki-latest-pages-articles.xml-*.txt_cleanuped.txt
rm -f jawiki-latest-pages-articles.xml-*.txt
rm -f jawiki-latest-pages-articles.xml.bz2

exit

# 分かちを入れる。
mv /root/docker-for-ai/ruby-dev/data/jawiki.txt /root/docker-for-ai/word2vec/data/.
word2vec-bash
# mecabのオプション(-b)でinput bufferを拡張しないとエラー(input-buffer overflow. The line is split. use -b #SIZE option.)となる。最大値は、8,192x640=5,242,880
# 約30分 jawiki_wakati.txtのサイズ: 約5.77GB(5,765,329,763)
time cat /var/lib/word2vec/jawiki.txt | mecab -b 5242880 -Owakati > /var/lib/word2vec/jawiki_wakati.txt
exit

# word2vecに学習させる。(単語数: 約9億個(912,134,318))
# 約54分 jawiki.binのサイズ: 約1.33GB(1,333,386,258)
time word2vec -train /var/lib/word2vec/jawiki_wakati.txt -output /var/lib/word2vec/jawiki.bin -size 200 -window 5 -negative 5 -hs 0 -sample 1e-3 -threads 8 -binary 1

# 中間ファイル削除
rm -f /root/docker-for-ai/word2vec/jawiki_wakati.txt
rm -f /root/docker-for-ai/word2vec/jawiki.txt
```
