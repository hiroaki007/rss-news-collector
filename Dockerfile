# ベースイメージ:軽量版(slim)を使用。フル版より軽く、alpine版よりトラブルが少ない、実務でよく使われるバランス
FROM python:3.12-slim

# タイムゾーンを日本時間に設定(cronを使う場合に必須。今回のプロジェクトでも必要)
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


# CMD ["python", "main.py"]


