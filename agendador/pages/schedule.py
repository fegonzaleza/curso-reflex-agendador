import reflex as rx
import sqlmodel
from ..components.navbar import navbar
from ..styles import styles
from ..models import Reserva

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00", "10:00", "11:00", "12:00",
         "13:00", "14:00", "15:00", "16:00", "17:00"]


class ScheduleState(rx.State):
    reservas: list[dict] = []

    show_modal: bool = False
    temp_dia: str = ""
    temp_hora: str = ""
    temp_nombre: str = ""

    def set_temp_nombre(self, value: str):
        self.temp_nombre = value

    @rx.var
    def ids_ocupados(self) -> list[str]:
        return [r["id"] for r in self.reservas]

    @rx.var
    def mapa_nombres(self) -> dict[str, str]:
        diccionario = {}
        for reserva in self.reservas:
            clave = reserva["id"]
            valor = reserva["nombre"]
            diccionario[clave] = valor
        return diccionario

    def cargar_reservas(self):
        with rx.session() as session:
            resultados = session.exec(sqlmodel.select(Reserva)).all()
            self.reservas = [
                {"id": f"{r.dia}-{r.hora}", "nombre": r.nombre_cliente}
                for r in resultados
            ]

    def abrir_modal(self, dia: str, hora: str):
        self.temp_dia = dia
        self.temp_hora = hora
        self.temp_nombre = ""
        self.show_modal = True

    def cerrar_modal(self):
        self.show_modal = False

    def guardar_reserva(self):
        with rx.session() as session:
            nueva = Reserva(
                dia=self.temp_dia,
                hora=self.temp_hora,
                nombre_cliente=self.temp_nombre
            )
            session.add(nueva)
            session.commit()

        self.show_modal = False
        self.cargar_reservas()

    def borrar_reserva(self, dia: str, hora: str):
        with rx.session() as session:
            consulta = sqlmodel.select(Reserva).where(
                (Reserva.dia == dia) & (Reserva.hora == hora)
            )
            obj = session.exec(consulta).first()
            if obj:
                session.delete(obj)
                session.commit()
        self.cargar_reservas()

    def manejar_click_celda(self, dia: str, hora: str):
        id_actual = f"{dia}-{hora}"
        es_ocupado = False
        for reserva in self.reservas:
            if reserva["id"] == id_actual:
                es_ocupado = True
                break

        if es_ocupado:
            self.borrar_reserva(dia, hora)
        else:
            self.abrir_modal(dia, hora)


# --- COMPONENTES VISUALES ---

def render_encabezado(texto: str):
    """Crea un encabezado con altura fija para evitar desalineaciones"""
    return rx.center(
        rx.text(texto, font_weight="bold", color=styles.ACCENT_COLOR),
        height="3em",  # <--- LA CLAVE: Altura fija para todos los títulos
        width="100%",
        # Un detallito visual extra
        border_bottom=f"1px solid {styles.ACCENT_COLOR}",
        margin_bottom="0.5em"
    )

# 1. NUEVA COLUMNA: Solo muestra las horas


def render_columna_horas():
    return rx.vstack(
        # Usamos el nuevo helper
        render_encabezado("Horario"),

        rx.foreach(
            HORAS,
            lambda h: rx.center(
                rx.text(h, color="gray", font_size="0.9em"),
                # MISMAS medidas que el botón (importante mantener el margin_y)
                height="3.5em",
                margin_y="0.2em",
                width="100%",
            )
        ),
        spacing="2",
        width="100%",
    )


def render_celda(dia: str, hora: str):
    id_actual = f"{dia}-{hora}"
    es_ocupado = ScheduleState.ids_ocupados.contains(id_actual)

    return rx.button(
        # 2. LÓGICA DE TEXTO: Nombre vs "Disponible"
        rx.cond(
            es_ocupado,
            # Caso Ocupado: Mostramos el nombre
            ScheduleState.mapa_nombres[id_actual],
            # Caso Libre: Mostramos "Disponible" en vez de la hora
            rx.text("Disponible", font_size="0.8em", opacity="0.5")
        ),

        on_click=lambda: ScheduleState.manejar_click_celda(dia, hora),
        color_scheme=rx.cond(es_ocupado, "green", "gray"),
        # Un toque extra: outline si está libre
        variant=rx.cond(es_ocupado, "solid", "classic"),
        width="100%",
        height="3.5em",
        margin_y="0.5em"
    )


def render_columna_dia(dia: str):
    return rx.vstack(
        # Reemplazamos rx.heading(dia...) por:
        render_encabezado(dia),

        rx.foreach(HORAS, lambda h: render_celda(dia, h)),

        spacing="2",
        width="100%",
    )


def schedule_page() -> rx.Component:
    return rx.box(
        navbar(),

        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Nueva Reserva"),
                rx.dialog.description(
                    f"Reservando para el {ScheduleState.temp_dia} a las {ScheduleState.temp_hora}"
                ),
                rx.flex(
                    rx.text("Nombre del Cliente:", margin_bottom="10px"),
                    rx.input(
                        placeholder="Ej: Juan Pérez",
                        value=ScheduleState.temp_nombre,
                        on_change=ScheduleState.set_temp_nombre
                    ),
                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", color_scheme="gray",
                                  on_click=ScheduleState.cerrar_modal)
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Guardar", on_click=ScheduleState.guardar_reserva)
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
            open=ScheduleState.show_modal,
        ),

        rx.vstack(
            rx.heading("Reserva tu Horario", size="8"),
            rx.text("Selecciona un bloque disponible para agendar."),

            # 3. CAMBIO EN LA GRILLA PRINCIPAL
            rx.grid(
                render_columna_horas(),  # <-- Agregamos la columna de horas al principio
                # <-- Luego las columnas de días
                rx.foreach(DIAS, render_columna_dia),

                # <-- Aumentamos a 6 columnas (1 de hora + 5 de días)
                columns="6",
                spacing="4",
                width="100%",
                max_width="1200px",  # Un poco más ancho para que quepa todo
            ),

            spacing="5",
            padding="2em",
            align_items="center",
            width="100%",
            on_mount=ScheduleState.cargar_reservas
        )
    )
