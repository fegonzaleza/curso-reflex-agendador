import reflex as rx
from .components.navbar import navbar
from .views.header import header_view
from .styles.styles import BASE_STYLE, STYLESHEETS


def index() -> rx.Component:
    return rx.box(
        navbar(),      # 1. Cargamos el componente Navbar
        header_view(),  # 2. Cargamos la vista del Header
    )


# Configuramos la app e inyectamos el estilo global
app = rx.App(
    stylesheets=STYLESHEETS,
    style=BASE_STYLE
)
app.add_page(index)
