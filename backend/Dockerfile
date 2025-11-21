FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    cmake \
    make \
    liblapack-dev \
    libblas-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

# u can also run it directly with python 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
