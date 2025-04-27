FROM python:3.11-slim

# Установка системных зависимостей для OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Сначала устанавливаем numpy 1.x, затем остальные зависимости
RUN pip install "numpy<2"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "ser1:app", "--host", "0.0.0.0", "--port", "8005"]
