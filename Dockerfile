FROM python:3.8

RUN pip config set global.index-url https://mirror.baidu.com/pypi/simple
COPY . /ml_work
WORKDIR /ml_work
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 nginx -y
RUN pip install -r requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/nginx_flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "api:app"]