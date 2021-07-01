FROM python:3.8

RUN pip config set global.index-url https://mirror.baidu.com/pypi/simple
COPY . /ml_work
WORKDIR /ml_work
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 nginx -y
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

RUN pip install -r requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/nginx_flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

#CMD 运行以下命令，daemon off后台运行，否则启动完就自动关闭
CMD ["nginx", "-g","daemon off;"]  
     
ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "api:app"]