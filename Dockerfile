FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# Entrypoint
CMD ["python3", "-u", "handler.py"]