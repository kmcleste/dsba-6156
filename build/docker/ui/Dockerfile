FROM python:3.9-slim
LABEL org.opencontainers.image.source="https://github.com/kmcleste/dsba-6156"

RUN mkdir -p app/logs && \
    apt-get update -yq

COPY src/ui app/src/ui
COPY build/docker/ui/requirements.txt /app/requirements.txt
COPY .streamlit /app/.streamlit

RUN python3 -m pip install -U pip && \
    python3 -m pip install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/ui/01_🏠_Home.py"]
