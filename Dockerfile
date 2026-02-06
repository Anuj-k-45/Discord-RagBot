FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/tmp/hf
ENV TRANSFORMERS_CACHE=/tmp/hf

WORKDIR /app

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
