# AI検証用Dockerコンテナ

各種AI検証用のDockerイメージを作成するためのDockerfile

## 動作環境
* OS: Ubuntu: 16.04
* GPU: GRID K520(NVIDIA): ドライババージョン: 367.57
* Docker: 0.12.1
* navidia-docker: 1.0.1-1
* git 2.6.2

## コードダウンロード
``` bash
cd /root
git clone https://github.com/koji77/docker-for-ai.git
```

## 内容
1. tf-cpu: Tensorflow実行環境(CPU版)
2. tf-gpu: Tensorflow実行環境(GPU版)
3. termextract: Termextract検証環境
4. word2vec: Word2Vec検証環境
5. ruby-dev: Ruby開発環境

## Commit & Push
``` bash
git add .
git commit -m "first commit"
# git remote add origin https://github.com/koji77/docker-for-ai.git
# git config http.postBuffer 524288000
# git push -u origin master
git push
```
