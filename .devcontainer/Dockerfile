FROM jupyter/all-spark-notebook:latest

LABEL project="ecommerce-dev"


USER root

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    wget \
    gnupg \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    && rm -rf /var/lib/apt/lists/*

    
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

USER jovyan
