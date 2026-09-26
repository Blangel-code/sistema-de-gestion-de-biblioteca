"""Vista visual de préstamos."""

import flet as ft

from components.modals import LoanFormDialog, ProcessLoanDialog
from config import PALETTE as COLORS

from querys import (
    change_status_loan,
    create_loan,
    search_loans,
    select_users_and_books_for_loans,
)

class LoansView(ft.Container):
    """Formulario de préstamo y listado de préstamos activos."""

    def __init__(self) -> None:
        self.header = self._header()
        self.search_field = ft.TextField(
            hint_text="Buscar por usuario o libro",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=8,
            on_change=self._refresh_table,
        )
        self.status_dropdown = ft.Dropdown(
            label="Estado",
            width=160,
            value="Todos",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Activo"),
                ft.dropdown.Option("Devuelto"),
                ft.dropdown.Option("Retrasado"),
            ],
            on_select=self._refresh_table,
        )
        self.table_card = ft.Container(self._active_loans_card(), expand=True)
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[
                    self._toolbar(),
                    self.table_card,
                ],
                spacing=16,
                expand=True,
            ),
        )

    def _header(self) -> ft.Column:
        return ft.Column(
            [
                ft.Text("Préstamos", size=26, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Controla los préstamos activos y las devoluciones",
                    size=13,
                    color=COLORS.TEXT_MUTED,
                ),
            ],
            spacing=3,
        )

    def _toolbar(self) -> ft.Row:
        return ft.Row(
            controls=[
                self.search_field,
                self.status_dropdown,
                ft.Button(
                    "Registrar préstamo",
                    icon=ft.Icons.ADD,
                    on_click=self._open_loan_dialog,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _open_loan_dialog(self, event: ft.ControlEvent) -> None:
        users, books = select_users_and_books_for_loans()
        self.dialog = LoanFormDialog(
            on_submit=lambda data: self._submit_loan(event.page, data),
            on_cancel=event.page.pop_dialog,
            options_users=users,
            options_books=books,
        )
        event.page.show_dialog(self.dialog)

    def _submit_loan(self, page: ft.Page, data: dict[str, str]) -> tuple[bool, str]:
        success, msg = create_loan(
            int(data["usuario"]),
            int(data["libro"]),
            data["fecha_devolucion"],
        )
        page.show_dialog(ft.SnackBar(msg))
        if not success:
            return
        self.dialog.open = False
        self._refresh_table()
        page.pop_dialog()

    def _refresh_table(self) -> None:
        self.table_card.content = self._active_loans_card()
        self.page.update()

    def _open_process_dialog(self, event: ft.ControlEvent, loan: dict[str, str]) -> None:
        self.dialog_process = ProcessLoanDialog(
            loan=loan,
            on_confirm=lambda: self._process_dialog(event.page,loan["prestamo_id"]),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(self.dialog_process)

    def _process_dialog(self,page:ft.Page, loan_id_to_complete:int) -> None:
        success, msg = change_status_loan(loan_id_to_complete)
        if not success:
            page.show_dialog(ft.SnackBar(msg))
            return
        self.dialog_process.open = False    
        self._refresh_table()

    def _active_loans_card(self) -> ft.Card:
        loans = search_loans(self.search_field.value,self.status_dropdown.value)
        rows = []
        for loan_id, name, card_id, title, status, loan_date, return_date, stored_status in loans:
            loan = {
                "prestamo_id": loan_id,
                "nombre": name,
                "cedula": card_id,
                "titulo": title,
                "estado": status,
                "fecha_de_prestamo": loan_date,
                "fecha_de_devolucion": return_date,
            }
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Column([ft.Text(name),ft.Text(card_id, style=ft.TextStyle(italic=True))],spacing=0)),
                        ft.DataCell(ft.Text(title,width=120,overflow=ft.TextOverflow.ELLIPSIS)),
                        ft.DataCell(ft.Text(loan_date)),
                        ft.DataCell(ft.Text(return_date)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(ft.OutlinedButton("Procesar devolución", on_click=lambda event, selected_loan=loan: self._open_process_dialog(event,selected_loan), icon=ft.Icons.CHECK), disabled=(stored_status == "Devuelto")),
                    ]
                )
            )
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Libro")),
                ft.DataColumn(ft.Text("Fecha préstamo")),
                ft.DataColumn(ft.Text("Fecha devolución")),
                ft.DataColumn(ft.Text("status")),
                ft.DataColumn(ft.Text("Acción")),
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
                    [
                        ft.Column(
                            controls=[
                                ft.Row([table], scroll=ft.ScrollMode.AUTO),
                            ],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ],
                    spacing=12,
                    expand=True,
                ),
            ),
        )
        
    @staticmethod
    def _status_badge(status: str) -> ft.Container:
        active = status == "Activo"
        overdue = status == "Retrasado"
        return ft.Container(
            content=ft.Text(
                status,
                size=12,
                color=COLORS.SUCCESS if active else COLORS.WARNING if overdue else COLORS.DANGER,
            ),
            bgcolor=COLORS.SUCCESS_BG if active else COLORS.WARNING_BG if overdue else COLORS.DANGER_BG,
            border_radius=12,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        )