FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD["streamlit","run","app.py","--server.port=8501","--server.address=192.168.1.5"]

