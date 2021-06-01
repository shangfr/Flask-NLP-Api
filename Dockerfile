FROM python:3.8

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
COPY . /app
WORKDIR /app
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]