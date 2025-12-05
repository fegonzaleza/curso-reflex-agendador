import reflex as rx
import os  # <--- Necesario para leer variables de entorno

# Leemos la variable de entorno DATABASE_URL
# Si no existe (ej: en tu PC sin configurar), usa sqlite local
database_url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="agendador",  # Asegúrate que este sea el nombre correcto de tu carpeta
    db_url=database_url,  # <--- Aquí asignamos la URL dinámica
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
