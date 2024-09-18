FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /blogcode

COPY requirements.txt /blogcode

RUN pip install --no-cache-dir -r requirements.txt

COPY src/flaskblog /blogcode/flaskblog

ENV FLASK_APP=flaskblog
ENV FLASK_ENV=production

EXPOSE 5000

CMD python3 main.py
