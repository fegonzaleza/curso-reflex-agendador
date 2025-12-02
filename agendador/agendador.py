import reflex as rx
from .components.navbar import navbar
from .views.header import header_view
from .views.todo import todo_view
from .pages.schedule import schedule_page  # <--- 1. NUEVO IMPORT
from .styles import styles


def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            header_view(),
            rx.divider(),
            todo_view(),
            spacing="5",
            align_items="center",
            width="100%",
            padding_bottom="4em"
        )
    )


app = rx.App(style=styles.BASE_STYLE, stylesheets=styles.STYLESHEETS)

# 2. DEFINICIÓN DE RUTAS
app.add_page(index, route="/")  # La raíz (Home)
app.add_page(schedule_page, route="/calendario")  # La nueva página
