import reflex as rx
from ..styles import styles


class TodoState(rx.State):
    # 1. Las variables (Memoria)
    tasks: list[str] = ["Aprender Reflex", "Configurar Git"]  # Lista inicial
    new_task: str = ""  # Variable temporal para lo que el usuario está escribiendo

    # 2. Las funciones (Lógica)
    def set_new_task(self, value: str):
        """Actualiza la variable temporal mientras escribes"""
        self.new_task = value

    def add_task(self):
        """Mueve el texto del input a la lista oficial"""
        if self.new_task:  # Si no está vacío
            self.tasks.append(self.new_task)
            self.new_task = ""  # Limpiamos el input

    def delete_task(self, task: str):
        """Borra una tarea de la lista"""
        self.tasks.remove(task)

# 3. Función auxiliar: Dibuja UNA sola fila de la lista


def render_item(task: str):
    return rx.hstack(
        rx.text(task, font_size="1.2em"),
        rx.spacer(),
        rx.button(
            "❌",
            on_click=lambda: TodoState.delete_task(
                task),  # Enviamos la tarea a borrar
            size="1",
            color_scheme="red",
            variant="ghost"
        ),
        width="100%",
        padding_y="0.5em",
        border_bottom="1px solid #333"
    )

# 4. La Vista Principal


def todo_view() -> rx.Component:
    return rx.vstack(
        rx.heading("Mi Agenda", size="6"),

        # --- Zona de Input ---
        rx.hstack(
            rx.input(
                placeholder="Nueva tarea...",
                value=TodoState.new_task,
                on_change=TodoState.set_new_task,  # Cada letra que escribes va al estado
                width="100%",
                bg="#252525",
                border="none"
            ),
            rx.button("Añadir", on_click=TodoState.add_task),
            width="100%",
        ),

        # --- Zona de Lista (Aquí ocurre la magia) ---
        rx.vstack(
            rx.foreach(
                TodoState.tasks,  # 1. Qué lista iterar
                render_item      # 2. Qué función usar para dibujar cada item
            ),
            width="100%",
            bg="#1e1e1e",
            padding="1em",
            border_radius="8px"
        ),

        width="100%",
        max_width="600px",  # Limitamos el ancho para que se vea bien
        spacing="4"
    )
