# Building from vanilla alpine base, as official Python
# alpine container is outdated and has 5 HIGH CVEs...
FROM alpine:latest

LABEL author="steveharsant"
LABEL org.opencontainers.image.description='Tide Invite - A Python script to invite friends to low tide windows'

ENV PYTHONUNBUFFERED=1

RUN mkdir /app /config
WORKDIR /app
COPY ./src /app/

RUN apk add python3 py3-pip tzdata && \
    pip install --no-cache-dir --break-system-packages -r /app/requirements.txt && \
    cp /usr/share/zoneinfo/Australia/Sydney /etc/localtime && \
    echo "Australia/Sydney" > /etc/timezone

CMD ["python", "/app/main.py"]