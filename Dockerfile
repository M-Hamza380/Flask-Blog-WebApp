FROM python:3.9-slim
WORKDIR /app
ENV FLASK_APP "main.py"
ENV FLASK_RUN_HOST "0.0.0.0"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
