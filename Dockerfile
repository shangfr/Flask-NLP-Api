FROM python:3.8

RUN pip config set global.index-url https://mirror.baidu.com/pypi/simple
COPY . /ml_work
WORKDIR /ml_work
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "api:app"]