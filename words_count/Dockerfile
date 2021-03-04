FROM python:3.7

#ENV PYTHONUNBUFFERED=1
#EXPOSE 5000

ADD . /django_app

WORKDIR /django_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update \
#    && apt-get add postgresql-dev gcc python3-dev musl-dev

RUN env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2==2.8.4


RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["/django_app/entrypoint.sh"]
