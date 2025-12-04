import reflex as rx

# --- CÓDIGO EXISTENTE DE RESERVA ---


class Reserva(rx.Model, table=True):
    dia: str
    hora: str
    nombre_cliente: str = ""

# --- NUEVO CÓDIGO PARA EL CHAT ---
# Creamos la tabla "Mensaje"


class Mensaje(rx.Model, table=True):
    usuario: str  # Quién lo escribió (ej: "Fernando")
    texto: str    # Qué escribió (ej: "Hola a todos")
    # Reflex agrega automáticamente un ID y la fecha de creación detrás de escena
