#!/bin/bash

# Укажите имя папки вашего проекта (как назовете репозиторий)
cd multimodal-agent

export PORT=5000
unset PIP_USER

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv --system-site-packages
fi

# Activate
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt || echo "Continuing..."
fi

echo "Starting application..."
python main.py