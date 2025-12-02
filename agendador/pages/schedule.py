import reflex as rx
from ..components.navbar import navbar
from ..styles import styles


def schedule_page() -> rx.Component:
    return rx.box(
        navbar(),  # <--- ¡Reutilizamos la barra de navegación!
        rx.vstack(
            rx.heading("Agenda Semanal", size="8"),
            rx.text("Aquí construiremos la grilla de horarios en el próximo módulo."),

            # Un placeholder visual para que no se vea vacío
            rx.center(
                rx.text("🚧 Espacio para el Calendario 🚧",
                        font_size="2em", opacity="0.3"),
                width="100%",
                height="300px",
                border=f"2px dashed {styles.ACCENT_COLOR}",
                border_radius="15px",
            ),

            spacing="5",
            padding="4em",
            align_items="center",
            width="100%"
        )
    )
