FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y python3-tk && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
