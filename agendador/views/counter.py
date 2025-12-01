import reflex as rx
from ..styles import styles

# 1. EL CEREBRO (State)
# Todo lo que cambia debe ir dentro de una clase que herede de rx.State


class CounterState(rx.State):
    count: int = 0  # Esta es la variable que cambiará (memoria)

    # Función para sumar (Event Handler)
    def increment(self):
        self.count += 1

    # Función para restar
    def decrement(self):
        self.count -= 1

# 2. EL CUERPO (Componente UI)


def counter_view() -> rx.Component:
    return rx.vstack(
        rx.heading("Contador Interactivo", size="7"),

        rx.hstack(
            # Botón Restar
            rx.button(
                "-",
                on_click=CounterState.decrement,  # Conectamos con el cerebro
                color_scheme="red",
                variant="soft"
            ),

            # El texto que muestra el valor actual del estado
            rx.text(
                CounterState.count,  # Leemos directamente del cerebro
                font_size="2em",
                font_weight="bold"
            ),

            # Botón Sumar
            rx.button(
                "+",
                on_click=CounterState.increment,  # Conectamos con el cerebro
                color_scheme="green",
                variant="soft"
            ),
            spacing="4",
        ),

        padding="2em",
        border=f"1px solid {styles.ACCENT_COLOR}",
        border_radius="10px",
        background_color="#1e1e1e",
        align_items="center",
    )
