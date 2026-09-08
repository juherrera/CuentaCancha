FROM python:3.12-slim

# Evita archivos .pyc y fuerza salida de logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# curl es necesario solo para el HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias primero (aprovecha cache de Docker si el código cambia pero no las deps)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Puerto en el que corre Streamlit
EXPOSE 8501

# Healthcheck opcional, útil si el cliente usa Docker Desktop y quiere ver el estado "healthy"
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Config para que Streamlit corra "headless" y sea accesible desde fuera del contenedor
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
