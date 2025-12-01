import reflex as rx
from .components.navbar import navbar
from .views.header import header_view
from .views.counter import counter_view
from .styles.styles import BASE_STYLE, STYLESHEETS


def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(            # Usamos vstack para apilar el header y el contador
            header_view(),
            rx.divider(),     # Una línea separadora visual
            counter_view(),   # <--- AQUI AGREGAMOS EL CONTADOR

            spacing="5",
            align_items='center',
            width="100%",
            padding_bottom="4em"
        ),
    )


# Configuramos la app e inyectamos el estilo global
app = rx.App(
    stylesheets=STYLESHEETS,
    style=BASE_STYLE
)
app.add_page(index)
