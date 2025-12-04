# import reflex as rx
# from ..components.navbar import navbar
# from ..styles import styles


# def schedule_page() -> rx.Component:
#     return rx.box(
#         navbar(),  # <--- ¡Reutilizamos la barra de navegación!
#         rx.vstack(
#             rx.heading("Agenda Semanal", size="8"),
#             rx.text("Aquí construiremos la grilla de horarios en el próximo módulo."),

#             # Un placeholder visual para que no se vea vacío
#             rx.center(
#                 rx.text("🚧 Espacio para el Calendario 🚧",
#                         font_size="2em", opacity="0.3"),
#                 width="100%",
#                 height="300px",
#                 border=f"2px dashed {styles.ACCENT_COLOR}",
#                 border_radius="15px",
#             ),
#             spacing="5",
#             padding="4em",
#             align_items="center",
#             width="100%"
#         )
#     )

import reflex as rx
from agendador.components.navbar import navbar
from ..styles import styles

# Definimos los datos fijos (Constantes)
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00", "10:00", "11:00", "12:00",
         "13:00", "14:00", "15:00", "16:00", "17:00"]


class ScheduleState(rx.State):
    # Lista de espacios reservados. Ej: ["Lunes-10:00", "Viernes-15:00"]
    reservas: list[str] = []

    def toggle_reserva(self, dia: str, hora: str):
        """Si ya existe la quita, si no existe la agrega"""
        clave = f"{dia}-{hora}"
        if clave in self.reservas:
            self.reservas.remove(clave)
        else:
            self.reservas.append(clave)

    def es_reservado(self, dia: str, hora: str) -> bool:
        """Helper para que la UI sepa si pintar verde o gris"""
        return list(self.reservas).contains(f"{dia}-{hora}")

# --- COMPONENTES VISUALES ---


def render_celda(dia: str, hora: str):
    """Dibuja un cuadradito individual (Slot)"""
    return rx.button(
        hora,
        # Si está reservado -> Verde, Si no -> Gris suave
        color_scheme=rx.cond(
            ScheduleState.reservas.contains(f"{dia}-{hora}"),
            "green",
            "gray"
        ),
        variant="solid",
        on_click=lambda: ScheduleState.toggle_reserva(dia, hora),
        width="100%",
        height="100%",
        min_height="50px",
    )


def render_columna_dia(dia: str):
    """Dibuja una columna entera: Título del día + Todas sus horas"""
    return rx.vstack(
        rx.heading(dia, size="4", color=styles.ACCENT_COLOR),
        # Aquí ocurre la magia: Iteramos las HORAS dentro de cada DÍA
        rx.foreach(
            HORAS,
            lambda h: render_celda(dia, h)
        ),
        spacing="2",
        width="100%",
        align_items="center"
    )

# --- PÁGINA PRINCIPAL ---


def schedule_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading("Reserva tu Horario", size="8"),
            rx.text(
                "Haz clic en las horas disponibles (Gris) para reservar (Verde)."),

            rx.divider(),

            # GRILLA PRINCIPAL
            # Usamos un Grid de 5 columnas (una por día)
            rx.grid(
                rx.foreach(
                    DIAS,
                    render_columna_dia
                ),
                columns="5",  # 5 columnas fijas
                spacing="4",
                width="100%",
                max_width="1000px",  # Que no se estire infinito en pantallas grandes
            ),

            spacing="5",
            padding="2em",
            align_items="center",
            width="100%"
        )
    )
