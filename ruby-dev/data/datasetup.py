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
            dst = re.sub(r'\d+\s+|\d*\.\d*|\[\d*\]|\.|,|\¥|!|\"|\'|#|\$|%|&|\+|\*|;|:|{|}|\?|~|\^|_|\||/|<|>|@|\(|\)|\[|\]|==|┃|┣|━|┳|┓|・|。|、|「|」|『|』|（|）|《|》|【|】|［|］|〈|〉|＝|：|；|／|～|→|●|≒|\[編集\]|\[隠す\]|\[非表示\]|\[ヘルプ\]|\[隠す\]|目次|詳細は|を参照|脚注|参考書籍|関連項目|関連作品|関連書籍|その他|外部リンク|表\s話\s編\s歴','\x20', src)
            # dst = re.sub(r'\s+','\u0020', dst)
            # 書き込みモードで開く(新規作成)
        with open(f + '_cleanuped.txt', 'w') as fd:
            # NFKC正規化
            dst = unicodedata.normalize('NFKC', dst)
            fd.write(dst)
            print(f + '_cleanuped.txt is successfully created')
