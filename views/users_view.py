"""Vista visual de usuarios."""

from collections.abc import Callable

import flet as ft

from components.modals import UserDetailsDialog, UserFormDialog, DeleteConfirmationDialog
from config import PALETTE as COLORS
from querys import add_user, search_users, eliminate_user

class UsersView(ft.Container):
    """Listado de usuarios con acciones de alta e importación."""

    def __init__(
        self,
        *,
        on_user_submit: Callable[[dict[str, str]], None] | None = None,
    ) -> None:
        self.on_user_submit = on_user_submit
        self.status_dropdown = ft.Dropdown(
            label="Estado",
            width=160,
            value="Todos",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Activo"),
                ft.dropdown.Option("Inactivo"),
            ],
            on_select=self._refresh_table,
        )
        self.search_field = ft.TextField(
            hint_text="Buscar usuario...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=8,
            on_change=self._refresh_table,
        )
        self.header = self._header()
        self.table_card = ft.Container(self._table_card(), expand=True)
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[self._filters(), self.table_card],
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
            on_submit=lambda data: self._submit_user(event.page, data),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _submit_user(
        self,
        page: ft.Page,
        data: dict[str, str],
    ) -> None:
        if self.on_user_submit is not None:
            self.on_user_submit(data)
        add_user(data)
        self._refresh_table()
        page.pop_dialog()

    def _filters(self) -> ft.Row:
        return ft.Row(
            controls=[
                self.search_field,
                self.status_dropdown,
            ],
            spacing=12,
        )

    def _refresh_table(self) -> None:
        """Refresca La Tabla De Los Usuarios Cada Vez Que Se Llama"""
        self.table_card.content = self._table_card()
        self.table_card.update()

    @staticmethod
    def _open_user_details(event: ft.ControlEvent, user: dict[str, str]) -> None:
        dialog = UserDetailsDialog(
            user=user,
            on_close=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _open_delete_dialog(self,event:ft.ControlEvent,delete_user: dict[str, str]) -> None:
        """Abre el menú de confirmación para eliminar un registro de un libro"""
        dialog = DeleteConfirmationDialog(
            item_name=delete_user["nombre"],
            on_confirm=lambda:self._delete_user(event.page,delete_user["id"]),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)
        
    def _delete_user(self,page:ft.Page,id_delete_user:int) -> None:
        """Elimina el registro del usuario en la base de datos"""
        eliminate_user(id_delete_user)
        self._refresh_table()
        page.pop_dialog()

    def _table_card(self) -> ft.Card:
        users = search_users(self.search_field.value,self.status_dropdown.value)
        
        rows = []
        for user_id, name, email, phone, id_card, status, registration_date in users:
            user = {
                "id": user_id,
                "nombre": name,
                "correo": email,
                "telefono": phone,
                "cedula": id_card,
                "estado": status,
                "fecha de registro": registration_date,
            }
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(user_id, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(email)),
                        ft.DataCell(ft.Text(phone)),
                        ft.DataCell(ft.Text(id_card)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Editar"),
                                    ft.IconButton(
                                        ft.Icons.VISIBILITY_OUTLINED,
                                        tooltip="Detalle",
                                        on_click=lambda event, selected_user=user: self._open_user_details(
                                            event,
                                            selected_user,
                                        ),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        tooltip="Eliminar",
                                        icon_color=COLORS.DANGER,
                                        on_click=lambda event, selected_user=user: self._open_delete_dialog(event,selected_user),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
            )
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Correo electrónico")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
            column_spacing=28,
            heading_row_color=COLORS.SURFACE_ALT,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=8,
            expand=True,
        )
        return ft.Card(
            elevation=0,
            expand=True,
            bgcolor=COLORS.SURFACE,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row([table], scroll=ft.ScrollMode.AUTO),
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
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
