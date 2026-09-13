"""Vista visual de préstamos."""

import flet as ft

from config import PALETTE as COLORS


class LoansView(ft.Container):
    """Formulario de préstamo y listado de préstamos activos."""

    def __init__(self) -> None:
        self.header = self._header()
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[
                    self._loan_form(),
                    self._active_loans_card(),
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

    def _loan_form(self) -> ft.Card:
        return ft.Card(
            elevation=0,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("Registrar préstamo", size=17, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.Dropdown(
                                    label="Usuario",
                                    hint_text="Selecciona un usuario",
                                    options=[
                                        ft.dropdown.Option("María González"),
                                        ft.dropdown.Option("Carlos Rodríguez"),
                                        ft.dropdown.Option("Ana Martínez"),
                                    ],
                                    expand=True,
                                ),
                                ft.Dropdown(
                                    label="Libro",
                                    hint_text="Selecciona un libro",
                                    options=[
                                        ft.dropdown.Option("El principito"),
                                        ft.dropdown.Option("Sapiens"),
                                        ft.dropdown.Option("Clean Code"),
                                    ],
                                    expand=True,
                                ),
                                ft.TextField(
                                    label="Fecha de devolución",
                                    hint_text="DD/MM/AAAA",
                                    prefix_icon=ft.Icons.CALENDAR_TODAY,
                                    expand=True,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "Registrar préstamo",
                                    icon=ft.Icons.ADD,
                                ),
                            ]
                        ),
                    ],
                    spacing=14,
                ),
            ),
        )

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
                        ft.Row([table], scroll=ft.ScrollMode.AUTO, expand=True),
                    ],
                    spacing=12,
                    expand=True,
                ),
            ),
        )
