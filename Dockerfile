FROM python:3.6-alpine

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/main' > /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories
RUN apk add --no-cache gcc musl-dev libgit2-dev libffi-dev

ADD . /microci
WORKDIR /microci

RUN python setup.py install

EXPOSE 8000

CMD gunicorn -w 4 -b 0.0.0.0:8000 microci.web.wsgi:app
