# 1. Usamos una base de Python oficial
FROM python:3.11-slim

# 2. Preparamos la carpeta de trabajo
WORKDIR /app

# 3. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA (Aquí estaba el fallo)
# Agregamos: unzip (para init), curl (para bajar cosas), nodejs/npm (para el frontend)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc unzip curl gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos los requisitos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos tu código
COPY . .

# 6. Inicializamos Reflex (Ahora sí funcionará porque tenemos unzip)
RUN reflex init

# 7. Ejecutamos en modo producción
CMD reflex run --env prod --backend-port $PORT --frontend-port $PORT