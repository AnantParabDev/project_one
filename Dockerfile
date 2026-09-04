FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY config/ ./config/
COPY controller/ ./controller/
COPY dao/ ./dao/
COPY models/ ./models/
COPY service/ ./service/
COPY templates/ ./templates/
COPY seed.py .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "app.py"]
