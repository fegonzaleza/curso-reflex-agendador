import reflex as rx
from ..styles import styles  # Importamos el archivo de estilos anterior


def navbar() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Agendador",
            font_size="1.5em",
            font_weight="bold",
            color=styles.ACCENT_COLOR
        ),
        rx.spacer(),  # Empuja lo siguiente a la derecha
        rx.button("Inicio", variant="ghost"),
        rx.button("Acerca de", variant="ghost"),

        position="sticky",
        top="0px",
        background_color=styles.PRIMARY_COLOR,
        padding="1em",
        z_index="5",
        border_bottom=f"1px solid {styles.ACCENT_COLOR}",
        width="100%",
    )
