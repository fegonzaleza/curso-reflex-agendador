# 1. Usamos Python ligero como base
FROM python:3.11-slim

# 2. Preparamos la carpeta
WORKDIR /app

# 3. Instalamos dependencias del sistema necesarias para Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos los requisitos e instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo tu código al contenedor
COPY . .

# 6. Inicializamos Reflex (crea carpetas necesarias)
RUN reflex init

# 7. Comando de arranque:
# --env prod: Modo producción (más rápido y seguro)
# --backend-port y --frontend-port: Usan el puerto que Render nos asigne ($PORT)
CMD reflex run --env prod --backend-port $PORT --frontend-port $PORT

