FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (match packages.txt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libsndfile1 \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Copy application
COPY . /app

EXPOSE 8501

# Default command uses $PORT if provided by platform
CMD ["/bin/sh", "-c", "streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
