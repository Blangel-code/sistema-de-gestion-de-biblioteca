"""Diálogos y paneles flotantes reutilizables."""

from collections.abc import Callable

import flet as ft
import re

from config import PALETTE as COLORS


class UserFormDialog(ft.AlertDialog):
    """Dialog para crear o editar un usuario."""

    def __init__(
        self,
        *,
        title: str = "Nuevo usuario",
        on_submit: Callable[[dict[str, str]], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.name_field = ft.TextField(label="Nombre completo", autofocus=True)
        self.gmail_field = ft.TextField(label="Correo Electrónico")
        self.phone_field = ft.TextField(label="Teléfono")
        self.id_card_field = ft.TextField(label="Cédula De Identidad")
        super().__init__(
            modal=True,
            title=ft.Text(title, color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=620,
                content=ft.Column(
                    [
                        ft.Row([self.name_field,self.gmail_field], spacing=12),
                        ft.Row([self.phone_field,self.id_card_field], spacing=12),
                    ],
                    tight=True,
                    spacing=14,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton("Guardar usuario", on_click=self._submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _submit(self, _: ft.ControlEvent) -> None:
        fields = {
            "name": self.name_field,
            "email": self.gmail_field,
            "phone": self.phone_field,
            "id_card": self.id_card_field,
        }
        invalid_fields = []

        for name, field in fields.items():
            value = (field.value or "").strip()
            field.error = None

            if not value:
                field.error = "Este campo es obligatorio."
                invalid_fields.append(name)
            elif name == "email" and not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",value):
                field.error = "El Email Ingresado No Es Valido."
                invalid_fields.append(name)
            elif name == "id_card" and not value.isdigit():
                field.error = "La Cédula Ingresada Solo Pueden Ser Números."
                invalid_fields.append(name)

        if invalid_fields:
            self.update()
            return

        if self.on_submit is not None:
            self.on_submit(
                {
                    "nombre": self.name_field.value or "",
                    "gmail": self.gmail_field.value or "",
                    "telefono": self.phone_field.value or "",
                    "cedula": self.id_card_field.value or "",
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


class BookFormDialog(ft.AlertDialog):
    """Dialog para registrar o editar un libro."""

    def __init__(
        self,
        *,
        title: str = "Nuevo libro",
        on_submit: Callable[[dict[str, str]], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.isbn_field = ft.TextField(label="ISBN", expand=True)
        self.title_field = ft.TextField(label="Título", expand=True)
        self.author_field = ft.TextField(label="Autor", expand=True)
        self.category_field = ft.TextField(label="Categoría", expand=True)
        self.year_field = ft.TextField(
            label="Año",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        self.pages_field = ft.TextField(
            label="Número de páginas",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        self.available_field = ft.TextField(
            label="Disponibles",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        self.publisher_field = ft.TextField(label="Editorial", expand=True)
        self.description_field = ft.TextField(
            label="Descripción",
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
        )
        super().__init__(
            modal=True,
            title=ft.Text(title, color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=520,
                content=ft.Column(
                    [
                        ft.Row(
                            [self.isbn_field, self.title_field],
                            spacing=12,
                        ),
                        ft.Row(
                            [self.author_field, self.category_field],
                            spacing=12,
                        ),
                        ft.Row(
                            [self.year_field, self.pages_field, self.publisher_field],
                            spacing=12,
                        ),
                        ft.Row(
                            [self.description_field, self.available_field],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    tight=True,
                    spacing=12,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton("Guardar libro", on_click=self._submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _submit(self, _: ft.ControlEvent) -> None:
        fields = {
            "isbn": self.isbn_field,
            "titulo": self.title_field,
            "autor": self.author_field,
            "descripcion": self.description_field,
            "categoria": self.category_field,
            "anio": self.year_field,
            "paginas": self.pages_field,
            "editorial": self.publisher_field,
            "disponibles": self.available_field,
        }
        numeric_fields = {"anio", "paginas", "disponibles"}
        invalid_fields = []

        for name, field in fields.items():
            value = (field.value or "").strip()
            field.error = None

            if not value and name != "disponibles":
                field.error = "Este campo es obligatorio."
                invalid_fields.append(name)
            elif name in numeric_fields and not value.isdigit():
                field.error = "Introduce un número entero."
                invalid_fields.append(name)

        if invalid_fields:
            self.update()
            return

        if self.on_submit is not None:
            self.on_submit(
                {
                    "isbn": self.isbn_field.value.strip() or "",
                    "titulo": self.title_field.value.strip() or "",
                    "autor": self.author_field.value.strip() or "",
                    "descripcion": self.description_field.value.strip() or "",
                    "categoria": self.category_field.value.strip().title() or "",
                    "anio": self.year_field.value.strip() or "",
                    "paginas": self.pages_field.value.strip() or "",
                    "editorial": self.publisher_field.value.strip() or "",
                    "disponibles": self.available_field.value.strip() or "0",
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


class LoanFormDialog(ft.AlertDialog):
    """Dialog para registrar un préstamo."""

    def __init__(
        self,
        *,
        on_submit: Callable[[dict[str, str]], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.user_field = ft.Dropdown(
            label="Usuario",
            hint_text="Selecciona un usuario",
            options=[
                ft.dropdown.Option("María González"),
                ft.dropdown.Option("Carlos Rodríguez"),
                ft.dropdown.Option("Ana Martínez"),
            ],
            expand=True,
        )
        self.book_field = ft.Dropdown(
            label="Libro",
            hint_text="Selecciona un libro",
            options=[
                ft.dropdown.Option("El principito"),
                ft.dropdown.Option("Sapiens"),
                ft.dropdown.Option("Clean Code"),
            ],
            expand=True,
        )
        self.return_date_field = ft.TextField(
            label="Fecha de devolución",
            hint_text="DD/MM/AAAA",
            prefix_icon=ft.Icons.CALENDAR_TODAY,
        )
        super().__init__(
            modal=True,
            title=ft.Text("Registrar préstamo", color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=560,
                content=ft.Column(
                    [
                        ft.Row(
                            [self.user_field, self.book_field],
                            spacing=12,
                        ),
                        self.return_date_field,
                    ],
                    tight=True,
                    spacing=14,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton("Registrar préstamo", icon=ft.Icons.ADD, on_click=self._submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _submit(self, _: ft.ControlEvent) -> None:
        if self.on_submit is not None:
            self.on_submit(
                {
                    "usuario": self.user_field.value or "",
                    "libro": self.book_field.value or "",
                    "fecha_devolucion": self.return_date_field.value or "",
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


class ProcessLoanDialog(ft.AlertDialog):
    """Dialog para procesar la devolución de un préstamo."""

    def __init__(
        self,
        *,
        loan: dict[str, str],
        on_confirm: Callable[[], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        super().__init__(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.SWAP_HORIZ_OUTLINED, color=COLORS.PRIMARY),
                    ft.Text("Procesar préstamo", color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=460,
                content=ft.Column(
                    [
                        ft.Text("Confirma la devolución de este registro:", color=COLORS.TEXT_MUTED),
                        self._detail_row("ID", loan["prestamo_id"]),
                        self._detail_row("Usuario", loan["nombre"]),
                        self._detail_row("Libro", loan["titulo"]),
                        self._detail_row("Fecha límite", loan["fecha_de_devolucion"]),
                    ],
                    tight=True,
                    spacing=12,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton(
                    "Procesar devolución",
                    icon=ft.Icons.CHECK,
                    on_click=self._confirm,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    @staticmethod
    def _detail_row(label: str, value: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(f"{label}:", weight=ft.FontWeight.BOLD, width=130),
                ft.Text(value, expand=True),
            ],
            spacing=10,
        )

    def _confirm(self, _: ft.ControlEvent) -> None:
        if self.on_confirm is not None:
            self.on_confirm()

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


class BookDetailsDialog(ft.AlertDialog):
    """Dialog de solo lectura con la información completa de un libro."""

    def __init__(
        self,
        *,
        book: dict[str, str],
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self.on_close = on_close
        super().__init__(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.MENU_BOOK_OUTLINED, color=COLORS.PRIMARY),
                    ft.Text("Información del libro", color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=560,
                content=ft.Column(
                    [
                        ft.Text(
                            book.get("titulo", "Sin título"),
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS.TEXT,
                        ),
                        self._detail_row("ISBN", book.get("isbn", "-")),
                        self._detail_row("Autor", book.get("autor", "-")),
                        self._detail_row("Categoría", book.get("categoria", "-")),
                        self._detail_row("Editorial", book.get("editorial", "-")),
                        self._detail_row("Año de publicación", book.get("anio", "-")),
                        self._detail_row("Páginas", book.get("paginas", "-")),
                        ft.Divider(height=8),
                        ft.Text("Descripción", weight=ft.FontWeight.BOLD, color=COLORS.TEXT),
                        ft.Text(
                            book.get("descripcion", "Sin descripción disponible."),
                            color=COLORS.TEXT_MUTED,
                        ),
                        ft.Row(
                            [
                                ft.Text("Estado", weight=ft.FontWeight.BOLD, color=COLORS.TEXT),
                                self._status_badge(book.get("estado", "Inactivo")),
                            ],
                            spacing=10,
                        ),
                    ],
                    tight=True,
                    spacing=12,
                ),
            ),
            actions=[ft.TextButton("Cerrar", on_click=self._close)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    @staticmethod
    def _detail_row(label: str, value: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(f"{label}:", weight=ft.FontWeight.BOLD, width=150),
                ft.Text(value, expand=True),
            ],
            spacing=10,
        )

    @staticmethod
    def _status_badge(status: str) -> ft.Container:
        active = status == "Activo"
        return ft.Container(
            content=ft.Text(
                status,
                size=12,
                color=COLORS.SUCCESS if active else COLORS.DANGER,
            ),
            bgcolor=COLORS.SUCCESS_BG if active else COLORS.DANGER_BG,
            border_radius=12,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        )

    def _close(self, _: ft.ControlEvent) -> None:
        if self.on_close is not None:
            self.on_close()


class UserDetailsDialog(ft.AlertDialog):
    """Dialog de solo lectura con la información completa de un usuario."""

    def __init__(
        self,
        *,
        user: dict[str, str],
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self.on_close = on_close
        super().__init__(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON_OUTLINE, color=COLORS.PRIMARY),
                    ft.Text(
                        "Información del usuario",
                        color=COLORS.TEXT,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=ft.Container(
                width=520,
                content=ft.Column(
                    [
                        ft.Text(
                            user.get("nombre", "Sin nombre"),
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS.TEXT,
                        ),
                        self._detail_row("ID", user.get("id", "-")),
                        self._detail_row("Correo electrónico", user.get("correo", "-")),
                        self._detail_row("Teléfono", user.get("telefono", "-")),
                        self._detail_row("Cédula", user.get("cedula", "-")),
                        ft.Divider(height=8),
                        self._detail_row("Fecha De Registro", user.get("fecha de registro")),
                        ft.Row(
                            [
                                ft.Text("Estado", weight=ft.FontWeight.BOLD, color=COLORS.TEXT),
                                self._status_badge(user.get("estado", "Inactivo")),
                            ],
                            spacing=10,
                        ),
                    ],
                    tight=True,
                    spacing=12,
                ),
            ),
            actions=[ft.TextButton("Cerrar", on_click=self._close)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    @staticmethod
    def _detail_row(label: str, value: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(f"{label}:", weight=ft.FontWeight.BOLD, width=170),
                ft.Text(value, expand=True),
            ],
            spacing=10,
        )

    @staticmethod
    def _status_badge(status: str) -> ft.Container:
        active = status == "Activo"
        return ft.Container(
            content=ft.Text(
                status,
                size=12,
                color=COLORS.SUCCESS if active else COLORS.DANGER,
            ),
            bgcolor=COLORS.SUCCESS_BG if active else COLORS.DANGER_BG,
            border_radius=12,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        )

    def _close(self, _: ft.ControlEvent) -> None:
        if self.on_close is not None:
            self.on_close()


class DeleteConfirmationDialog(ft.AlertDialog):
    """Dialog de confirmación para eliminar un registro."""

    def __init__(
        self,
        *,
        item_name: str = "este elemento",
        on_confirm: Callable[[], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        super().__init__(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=COLORS.WARNING),
                    ft.Text("Confirmar eliminación", weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            content=ft.Text(
                f"¿Estás seguro de que deseas eliminar {item_name}? "
                "Esta acción no se puede deshacer."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE_OUTLINE,
                    bgcolor=COLORS.DANGER,
                    color=ft.Colors.WHITE,
                    on_click=self._confirm,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _confirm(self, _: ft.ControlEvent) -> None:
        if self.on_confirm is not None:
            self.on_confirm()

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


class UserOptionsSheet(ft.BottomSheet):
    """Menú flotante con acciones para una cuenta de usuario."""

    def __init__(
        self,
        *,
        on_history: Callable[[], None] | None = None,
        on_suspend: Callable[[], None] | None = None,
        on_reminder: Callable[[], None] | None = None,
    ) -> None:
        self.on_history = on_history
        self.on_suspend = on_suspend
        self.on_reminder = on_reminder
        super().__init__(
            content=ft.Container(
                padding=ft.Padding.only(left=22, right=22, top=18, bottom=24),
                content=ft.Column(
                    [
                        ft.Text("Opciones de usuario", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=8),
                        self._action(
                            ft.Icons.HISTORY,
                            "Ver historial",
                            self._history,
                        ),
                        self._action(
                            ft.Icons.BLOCK_OUTLINED,
                            "Suspender cuenta",
                            self._suspend,
                        ),
                        self._action(
                            ft.Icons.NOTIFICATIONS_OUTLINED,
                            "Enviar recordatorio",
                            self._reminder,
                        ),
                    ],
                    tight=True,
                    spacing=4,
                ),
            ),
            open=False,
            show_drag_handle=True,
        )

    @staticmethod
    def _action(
        icon: str,
        label: str,
        handler: Callable[[ft.ControlEvent], None],
    ) -> ft.ListTile:
        return ft.ListTile(
            leading=ft.Icon(icon, color=COLORS.PRIMARY),
            title=ft.Text(label),
            on_click=handler,
        )

    def _history(self, _: ft.ControlEvent) -> None:
        if self.on_history is not None:
            self.on_history()

    def _suspend(self, _: ft.ControlEvent) -> None:
        if self.on_suspend is not None:
            self.on_suspend()

    def _reminder(self, _: ft.ControlEvent) -> None:
        if self.on_reminder is not None:
            self.on_reminder()


class AdvancedFilterDialog(ft.AlertDialog):
    """Panel de filtros avanzados para libros o usuarios."""

    def __init__(
        self,
        *,
        on_apply: Callable[[dict[str, object]], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        self.on_apply = on_apply
        self.on_cancel = on_cancel
        self.category = ft.Dropdown(
            label="Categoría",
            options=[
                ft.dropdown.Option("Todas"),
                ft.dropdown.Option("Ficción"),
                ft.dropdown.Option("Historia"),
                ft.dropdown.Option("Ciencia"),
                ft.dropdown.Option("Tecnología"),
            ],
            value="Todas",
        )
        self.status = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Activo"),
                ft.dropdown.Option("Inactivo"),
            ],
            value="Todos",
        )
        self.available_only = ft.Checkbox(label="Mostrar solo disponibles")
        self.overdue_only = ft.Checkbox(label="Mostrar préstamos vencidos")
        super().__init__(
            modal=True,
            title=ft.Text("Filtros avanzados", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=460,
                content=ft.Column(
                    [
                        ft.Text("Refina los resultados de la vista", color=COLORS.TEXT_MUTED),
                        ft.Row([self.category, self.status], spacing=12),
                        self.available_only,
                        self.overdue_only,
                    ],
                    tight=True,
                    spacing=12,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton("Aplicar filtros", on_click=self._apply),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _apply(self, _: ft.ControlEvent) -> None:
        if self.on_apply is not None:
            self.on_apply(
                {
                    "categoria": self.category.value or "Todas",
                    "estado": self.status.value or "Todos",
                    "solo_disponibles": self.available_only.value,
                    "solo_vencidos": self.overdue_only.value,
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()
