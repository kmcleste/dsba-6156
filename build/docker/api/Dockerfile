FROM python:3.9-slim
LABEL org.opencontainers.image.source="https://github.com/kmcleste/dsba-6156"

RUN mkdir -p app/logs

RUN apt-get update -y -qq && \
    apt-get install git g++ ffmpeg libsndfile1 xpdf -y -qq

COPY src/api app/src/api
COPY build/docker/api/requirements.txt /app/requirements.txt

RUN python3 -m pip install -U pip && \
    python3 -m pip install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src/api/"]
