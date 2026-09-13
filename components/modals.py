"""Diálogos y paneles flotantes reutilizables."""

from collections.abc import Callable

import flet as ft

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
        self.role_field = ft.Dropdown(
            label="Rol",
            options=[
                ft.dropdown.Option("Administrador"),
                ft.dropdown.Option("Bibliotecario"),
                ft.dropdown.Option("Lector"),
            ],
        )
        self.year_field = ft.TextField(label="Año de registro", keyboard_type=ft.KeyboardType.NUMBER, hint_text="YYYY/MM/DD")
        super().__init__(
            modal=True,
            title=ft.Text(title, color=COLORS.TEXT, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=520,
                content=ft.Column(
                    [
                        self.name_field,
                        self.gmail_field,
                        self.phone_field,
                        ft.Row([self.role_field, self.year_field], spacing=12),
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
        if self.on_submit is not None:
            self.on_submit(
                {
                    "nombre": self.name_field.value or "",
                    "gmail": self.gmail_field.value or "",
                    "telefono": self.phone_field.value or "",
                    "role": self.role_field.value or "",
                    "anio": self.year_field.value or "",
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()


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
