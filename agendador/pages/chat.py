import reflex as rx
import sqlmodel
from ..components.navbar import navbar
from ..styles import styles
from ..models import Mensaje


class ChatState(rx.State):
    mensajes: list[dict] = []
    mensaje_nuevo: str = ""
    usuario_actual: str = "Invitado"  # Nombre por defecto

    def set_mensaje_nuevo(self, valor: str):
        self.mensaje_nuevo = valor

    # --- NUEVO: Función para cambiar quién soy ---
    def set_usuario_actual(self, valor: str):
        self.usuario_actual = valor

    def cargar_mensajes(self):
        """Esta función ahora será llamada automáticamente cada 2 seg"""
        with rx.session() as session:
            resultados = session.exec(sqlmodel.select(Mensaje)).all()
            self.mensajes = [
                {"usuario": m.usuario, "texto": m.texto}
                for m in resultados
            ]

    def enviar_mensaje(self):
        if self.mensaje_nuevo == "":
            return

        with rx.session() as session:
            nuevo = Mensaje(
                usuario=self.usuario_actual,
                texto=self.mensaje_nuevo
            )
            session.add(nuevo)
            session.commit()

        self.mensaje_nuevo = ""
        self.cargar_mensajes()

# --- DISEÑO DEL MENSAJE INTELIGENTE ---


def render_mensaje(mensaje: dict):
    # Pregunta Clave: ¿Fui yo quien escribió esto?
    # Reflex necesita que esta comparación sea una Var para el frontend
    es_mio = mensaje["usuario"] == ChatState.usuario_actual

    return rx.flex(
        # Globito del mensaje
        rx.box(
            rx.text(
                mensaje["usuario"],
                font_weight="bold",
                font_size="0.7em",
                # Color nombre sutil
                color=rx.cond(es_mio, "#e0f2f1", "#a0aec0")
            ),
            rx.text(mensaje["texto"]),

            # --- ESTILOS DINÁMICOS ---
            # Si es mío: Verde. Si no: Gris.
            background_color=rx.cond(es_mio, styles.ACCENT_COLOR, "#333"),
            # Si es mío: Texto blanco. Si no: Texto gris claro.
            color="white",

            padding_x="1em",
            padding_y="0.5em",
            border_radius="15px",

            # Truco visual: La "colita" del globo cambia de lado
            border_bottom_right_radius=rx.cond(es_mio, "0px", "15px"),
            border_bottom_left_radius=rx.cond(es_mio, "15px", "0px"),

            width="fit-content",
            max_width="80%",
        ),

        # --- ALINEACIÓN ---
        # Si es mío: Alineado a la derecha (end). Si no: A la izquierda (start).
        justify=rx.cond(es_mio, "end", "start"),
        width="100%",
        margin_bottom="0.5em",
    )


def chat_page() -> rx.Component:
    return rx.box(
        navbar(),

        # --- EL MOTOR DE TIEMPO REAL (POLLING) ---
        # Este componente es invisible (display="none").
        # Su único trabajo es activar un evento cada 2000ms (2 segundos).
        rx.moment(
            interval=2000,
            on_change=ChatState.cargar_mensajes,
            display="none"
        ),
        # -----------------------------------------

        rx.vstack(
            rx.heading("Sala de Chat", size="8"),

            # --- ZONA DE IDENTIDAD (Para pruebas) ---
            rx.hstack(
                rx.text("Tu nombre:", font_weight="bold"),
                rx.input(
                    value=ChatState.usuario_actual,
                    on_change=ChatState.set_usuario_actual,
                    width="150px",
                    # bg="#222"
                ),
                rx.text("(Cámbialo para simular ser otra persona)",
                        font_size="0.8em", opacity="0.6"),
                align_items="center",
                margin_bottom="1em"
            ),

            # --- ZONA DE MENSAJES ---
            rx.vstack(
                rx.foreach(ChatState.mensajes, render_mensaje),
                width="100%",
                height="50vh",
                overflow_y="auto",
                border="1px solid #444",
                padding="1em",
                border_radius="10px",
                background_color="#1a1a1a",
            ),

            # --- ZONA DE ESCRITURA ---
            rx.hstack(
                rx.input(
                    placeholder="Escribe algo...",
                    value=ChatState.mensaje_nuevo,
                    on_change=ChatState.set_mensaje_nuevo,
                    width="100%"
                ),
                rx.button("Enviar", on_click=ChatState.enviar_mensaje,
                          cursor="pointer"),
                width="100%",
                padding_top="1em"
            ),

            width="100%",
            max_width="800px",
            padding="2em",
            align_items="center",
            on_mount=ChatState.cargar_mensajes
        )
    )
