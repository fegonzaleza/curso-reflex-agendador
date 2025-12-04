import reflex as rx

# Creamos una tabla llamada "Reserva"
# rx.Model le dice a Reflex que esto debe convertirse en una tabla de base de datos


class Reserva(rx.Model, table=True):
    dia: str
    hora: str
    nombre_cliente: str = ""  # <--- NUEVO CAMPO (Por defecto vacío)
