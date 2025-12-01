import reflex as rx
from ..styles import styles


def header_view() -> rx.Component:
    return rx.vstack(
        rx.heading("Gestiona tu tiempo", size="9"),
        rx.text(
            "La forma más simple de agendar tus citas y organizar tu semana.",
            font_size="1.2em",
            opacity="0.8"
        ),
        rx.button(
            "Comenzar ahora",
            background_color=styles.ACCENT_COLOR,
            color="white",
            padding="1em",
            border_radius="8px"
        ),
        spacing="5",  # Espacio entre elementos (1-9)
        padding_top="5em",
        align_items="center",  # Centra el contenido horizontalmente
        text_align="center",
        width="100%",
    )
