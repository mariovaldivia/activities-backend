FROM python:3.10.6-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY . /code/
RUN apk update
# RUN apk add gcc libc-dev g++ libffi-dev libxml2 curl gnupg python3-dev openssl-dev libressl-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers  \
    && apk add libffi-dev python3-dev openssl-dev libressl-dev
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \

    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8008", "--chdir", "app", "app.wsgi:application"]