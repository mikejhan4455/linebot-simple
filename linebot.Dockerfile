FROM alpine:latest

MAINTAINER Chris Zhan mikejhan.net

WORKDIR /app

COPY ./sources/* /app/
COPY ./requirements.txt /app/

ENV CHANNEL_ACCESS_TOKEN=null
ENV CHANNEL_SERECT=null

RUN apk add python3 \
  && apk add libffi-dev openssl-dev \
  && apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev \
  && pip3 install --upgrade pip \
  && pip3 install --upgrade setuptools \
  && pip3 install --no-cache-dir -r /app/requirements.txt \
  && apk del .pynacl_deps \
  && rm requirements.txt

EXPOSE 3001

CMD [ "python3", "/app/line.py"]

