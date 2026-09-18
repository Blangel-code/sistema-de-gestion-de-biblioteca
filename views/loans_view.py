"""Vista visual de préstamos."""

import flet as ft

from components.modals import LoanFormDialog, ProcessLoanDialog
from config import PALETTE as COLORS


class LoansView(ft.Container):
    """Formulario de préstamo y listado de préstamos activos."""

    def __init__(self) -> None:
        self.header = self._header()
        self.search_field = ft.TextField(
            hint_text="Buscar por usuario, libro o ID",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=8,
            on_change=lambda _: self._refresh_table(),
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
            on_confirm=event.page.pop_dialog,
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _active_loans_card(self) -> ft.Card:
        loans = [
            ("P-1001", "María González", "El principito", "12/09/2026", "20/09/2026"),
            ("P-1002", "Carlos Rodríguez", "Sapiens", "10/09/2026", "18/09/2026"),
            ("P-1003", "Ana Martínez", "Clean Code", "08/09/2026", "16/09/2026"),
        ]
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(loan_id, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(user)),
                    ft.DataCell(ft.Text(book)),
                    ft.DataCell(ft.Text(loan_date)),
                    ft.DataCell(ft.Text(return_date)),
                    ft.DataCell(ft.OutlinedButton("Procesar devolución", icon=ft.Icons.CHECK)),
                ]
            )
            for loan_id, user, book, loan_date, return_date in loans
        ]
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Libro")),
                ft.DataColumn(ft.Text("Fecha préstamo")),
                ft.DataColumn(ft.Text("Fecha devolución")),
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
                        ft.Text("Préstamos activos", size=17, weight=ft.FontWeight.BOLD),
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
