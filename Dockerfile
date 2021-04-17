FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2020-12-19
RUN apk --update add bash nano 
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
ENV AWS_DEFAULT_REGION us-east-1
COPY . /app
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt