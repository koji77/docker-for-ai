# tf-gpu: Tensorflow実行環境(GPU版)

## コンテナの構成
* OS: Ubuntu: 16.04
* Python: 3.5
* CUDA: 8.0
* cuDNN: 5.0
* Tensorfolw: 0.12.1

## Dockerイメージ作成
``` bash
cd /root/docker-for-ai/tf-gpu
nvidia-docker build --tag="29koji/tf-gpu" .
```

## Dockerコンテナ作成&実行
``` bash
nvidia-docker run -d --name tf-gpu -p 8888:8888 -p 6006:6006 -v /root/docker-for-ai/tf-gpu/data/notebooks:/notebooks -e PASSWORD=pass 29koji/tf-gpu
```

## Jupyterアクセス
* ブラウザでhttp://<your host address>:8888へアクセス
