FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libre2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
