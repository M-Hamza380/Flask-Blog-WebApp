FROM python:3.9-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.9-slim

RUN useradd -m -s /bin/bash -c "Muhammad Hamza Anjum,hamza.anjum380@gmail.com" mhamza380

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY src/flaskblog /app/flaskblog

ENV FLASK_APP=flaskblog
ENV FLASK_ENV=production

USER mhamza380

EXPOSE 5000

CMD ["python", "main.py"]
