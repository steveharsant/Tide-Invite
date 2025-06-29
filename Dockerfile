# Building from vanilla alpine base, as official Python
# alpine container is outdated and has 5 HIGH CVEs...
FROM alpine:latest

LABEL author="steveharsant"
LABEL org.opencontainers.image.description='Tide Invite - A Python script to invite friends to low tide windows'

RUN mkdir /app /config
WORKDIR /app
COPY ./src /app/

RUN apk add python3 py3-pip && \
    pip install --no-cache-dir --break-system-packages -r /app/requirements.txt

CMD ["python", "/app/main.py"]