FROM python:3.9-slim
LABEL org.opencontainers.image.source="https://github.com/kmcleste/dsba-6156"

RUN mkdir -p app/logs

COPY src/ app/
COPY build/requirements.txt /app/requirements.txt
COPY build/docker/entrypoint.sh /app/entrypoint.sh

RUN apt-get update -y -qq && \
    python3 -m pip install -U pip && \
    python3 -m pip install -r /app/requirements.txt && \
    chmod +x /app/entrypoint.sh

WORKDIR /app

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
