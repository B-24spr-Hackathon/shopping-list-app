# Pythonのイメージ。Debian Bullseyeをベースに指定
FROM python:3.11-bullseye

# Pythonの出力がDockerのログとして扱われる
ENV PYTHONUNBUFFERED 1

# pycacheの生成を行わない
ENV PYTHONDONTWRITEBYTECODE 1

# 作業ディレクトリ
WORKDIR /backend

# Pythonの依存関係をコピー
COPY requirements.txt /backend/

# パッケージのインストール
RUN pip install -r requirements.txt

# 現在のディレクトリをbackendディレクトリにコピー
COPY . /backend/