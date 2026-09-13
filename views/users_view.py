"""Vista visual de usuarios."""

from collections.abc import Callable

import flet as ft

from components.modals import UserFormDialog
from config import PALETTE as COLORS


class UsersView(ft.Container):
    """Listado de usuarios con acciones de alta e importación."""

    def __init__(
        self,
        *,
        on_user_submit: Callable[[dict[str, str]], None] | None = None,
    ) -> None:
        self.on_user_submit = on_user_submit
        self.header = self._header()
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[self._filters(), self._table_card()],
                spacing=16,
                expand=True,
            ),
        )

    def _header(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Column(
                    [
                        ft.Text("Usuarios", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Administra los miembros registrados",
                            size=13,
                            color=COLORS.TEXT_MUTED,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.OutlinedButton("Importar Usuarios", icon=ft.Icons.UPLOAD_FILE),
                ft.ElevatedButton(
                    "Nuevo Usuario",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=self._open_user_dialog,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _open_user_dialog(self, event: ft.ControlEvent) -> None:
        """Abre el formulario modal usando la página asociada al evento."""
        dialog = UserFormDialog(
            on_submit=lambda data: self._submit_user(event.page, dialog, data),
            on_cancel=lambda: self._close_dialog(event.page, dialog),
        )
        event.page.show_dialog(dialog)

    def _submit_user(
        self,
        page: ft.Page,
        dialog: UserFormDialog,
        data: dict[str, str],
    ) -> None:
        if self.on_user_submit is not None:
            self.on_user_submit(data)
        self._close_dialog(page, dialog)

    @staticmethod
    def _close_dialog(page: ft.Page, dialog: UserFormDialog) -> None:
        page.pop_dialog()

    def _filters(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.TextField(
                    hint_text="Buscar usuario...",
                    prefix_icon=ft.Icons.SEARCH,
                    expand=True,
                    border_radius=8,
                ),
                ft.Dropdown(
                    label="Estado",
                    width=160,
                    value="Todos",
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Activo"),
                        ft.dropdown.Option("Inactivo"),
                    ],
                ),
            ],
            spacing=12,
        )

    def _table_card(self) -> ft.Card:
        users = [
            ("U-001", "María González", "maria@email.com", "555-0101", "Activo"),
            ("U-002", "Carlos Rodríguez", "carlos@email.com", "555-0102", "Activo"),
            ("U-003", "Ana Martínez", "ana@email.com", "555-0103", "Activo"),
            ("U-004", "Luis Herrera", "luis@email.com", "555-0104", "Inactivo"),
        ]
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(user_id, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(ft.Text(email)),
                    ft.DataCell(ft.Text(phone)),
                    ft.DataCell(self._status_badge(status)),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Editar"),
                                ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, tooltip="Detalle"),
                            ],
                            spacing=0,
                        )
                    ),
                ]
            )
            for user_id, name, email, phone, status in users
        ]
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Correo electrónico")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
            column_spacing=28,
            heading_row_color=COLORS.SURFACE_ALT,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=8,
        )
        return ft.Card(
            elevation=0,
            expand=True,
            bgcolor=COLORS.SURFACE,
            content=ft.Container(
                content=ft.Row([table], scroll=ft.ScrollMode.AUTO, expand=True),
                padding=8,
                expand=True,
            ),
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
