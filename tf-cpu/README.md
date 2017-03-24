# tf-cpu: Tensorflow実行環境(CPU版)

## 動作環境
* OS: Ubuntu: 16.04
* Python: 3.5
* Tensorfolw: 0.12.1

## Dockerイメージ作成
``` bash
cd /root/docker-for-ai/tf-cpu
docker build --tag="29koji/tf-cpu" .
```

## Dockerコンテナ作成&実行
``` bash
docker run -d --name tf-cpu -p 8888:8888 -p 6006:6006 -v ~/docker-for-ai/tf-cpu/data/notebooks:/notebooks -e PASSWORD=pass 29koji/tf-cpu
```

## Jupyterアクセス
* ブラウザでhttp://<your host address>:8888へアクセス
