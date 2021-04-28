FROM python:3.8

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]