# coding: utf-8
# 出力したファイルを「cat *.txt > data.txt」で連結する。

# モジュール属性argvを取得する
import sys
import re
import glob
import unicodedata

# コマンドライン引数を格納したリストの取得
argvs = sys.argv
# 引数の個数
argc = len(argvs)

if argc < 2:
    print('Invarid argument')
    sys.exit()

for i, v in enumerate(argvs):
    if i == 0:
        continue
    files = glob.glob(v)
    for f in files:
        dst = ''
        # 読み込みモードで開く
        with open(f, 'r') as fs:
            src = fs.read()
            # utf-8以外の文字を潰す。
            # str文字列に対してdecode()メソッドを呼び出すとunicode文字列が得られる。
            dst = src.decode('utf-8', 'ignore')
            # ハイフネーションを潰す。(紙のテキストではあり得るがWebページではないので実行しない。)
            # dst = re.sub('-[\r\n]+', '', dst)
            # 改行・改頁を潰す。
            dst = re.sub('[\r\n\x0c]+', '', dst)
            # 項番を潰す。
            dst = re.sub('\d*\.\d*\s', '', dst)
            # 統一的な題目を潰す。
            dst = re.sub(r'\[編集\]\s|\[隠す\]\s|\[非表示\]\s|\[ヘルプ\]\s|\[隠す\]\s|目次\s|詳細は|を参照|脚注\s|参考書籍\s|関連項目\s|関連作品\s|関連書籍\s|その他\s|外部リンク\s|表\s話\s編\s歴\s', '', dst)
            # 記号を空白に置き換える。
            # dst = re.sub('\.|,|\¥|!|\"|\'|#|\$|%|&|\+|\*|;|:|{|}|\?|~|\^|_|\||/|<|>|@|\(|\)|\[|\]|==|\.\.\.+', '', dst)
            dst = re.sub(r'[\.\,\¥\!\"\'\#\$%&\+\*;\:\{\}\?~\^_\\/\<\>\@()\[\]\=\-]', '', dst)
            # 全角記号を空白に置き換える。(除: 句点)
            dst = re.sub(r'[┃┣━┳┓・、「」『』（）《》【】［］〈〉＝：；／～→●≒]', '', dst)
            # 空白文字(空白、改行、改頁)が連続したら空白1つに置き換える。
            # dst = re.sub('\s+', ' ', dst)
            # 句点(。)で行を分割する。
            dst = re.sub(u'。', u'。' + '\n', dst)
        # 書き込みモードで開く(新規作成)
        with open(f + '_cleanuped.txt', 'w') as fd:
            # NFKC正規化
            dst = unicodedata.normalize('NFKC', dst)
            fd.write(dst.encode('utf_8'))
            print(f + '_cleanuped.txt is successfully created')
