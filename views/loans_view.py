"""Vista visual de préstamos."""

import flet as ft

from components.modals import LoanFormDialog, ProcessLoanDialog
from config import PALETTE as COLORS

from querys import search_loans, change_status_loan

class LoansView(ft.Container):
    """Formulario de préstamo y listado de préstamos activos."""

    def __init__(self) -> None:
        self.header = self._header()
        self.search_field = ft.TextField(
            hint_text="Buscar por usuario, libro o ID",
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
                ft.ElevatedButton(
                    "Registrar préstamo",
                    icon=ft.Icons.ADD,
                    on_click=self._open_loan_dialog,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _open_loan_dialog(self, event: ft.ControlEvent) -> None:
        dialog = LoanFormDialog(
            on_submit=lambda data: self._submit_loan(event.page),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _submit_loan(self, page: ft.Page) -> None:
        page.pop_dialog()

    def _refresh_table(self) -> None:
        self.table_card.content = self._active_loans_card()
        self.table_card.update()

    def _open_process_dialog(self, event: ft.ControlEvent, loan: dict[str, str]) -> None:
        dialog = ProcessLoanDialog(
            loan=loan,
            on_confirm=lambda: self._process_dialog(event.page,loan["prestamo_id"]),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _process_dialog(self,page:ft.Page, loan_id_to_complete:int) -> None:
        change_status_loan(loan_id_to_complete)
        self._refresh_table()
        page.pop_dialog()

    def _active_loans_card(self) -> ft.Card:
        loans = search_loans(self.search_field.value,self.status_dropdown.value)
        rows = []
        for loan_id, name, card_id, title, status, loan_date, return_date in loans:
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
                        ft.DataCell(ft.Text(loan_id, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Column([ft.Text(name),ft.Text(card_id, style=ft.TextStyle(italic=True))],spacing=0)),
                        ft.DataCell(ft.Text(title)),
                        ft.DataCell(ft.Text(loan_date)),
                        ft.DataCell(ft.Text(return_date)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(ft.OutlinedButton("Procesar devolución", on_click=lambda event, selected_loan=loan: self._open_process_dialog(event,selected_loan), icon=ft.Icons.CHECK), disabled=(status == "Devuelto")),
                    ]
                )
            )
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
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
                padding=16,
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