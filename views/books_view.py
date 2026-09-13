"""Vista visual del catálogo de libros."""

import flet as ft

from config import PALETTE as COLORS


class BooksView(ft.Container):
    """Catálogo con búsqueda, filtros y acciones por libro."""

    def __init__(self) -> None:
        self.header = self._header()
        self.search_field = ft.TextField(
            hint_text="Buscar por título, autor o ISBN",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=8,
        )
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[
                    self._filters(),
                    self._table_card(),
                ],
                spacing=16,
                expand=True,
            ),
        )

    def _header(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Libros", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Consulta y organiza el catálogo",
                            size=13,
                            color=COLORS.TEXT_MUTED,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Añadir Libro",
                    icon=ft.Icons.ADD,
                    on_click=lambda _: None,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _filters(self) -> ft.Row:
        return ft.Row(
            controls=[
                self.search_field,
                ft.Dropdown(
                    label="Categoría",
                    width=170,
                    options=[
                        ft.dropdown.Option("Todas"),
                        ft.dropdown.Option("Ficción"),
                        ft.dropdown.Option("Historia"),
                        ft.dropdown.Option("Ciencia"),
                        ft.dropdown.Option("Tecnología"),
                    ],
                    value="Todas",
                ),
                ft.Dropdown(
                    label="Estado",
                    width=150,
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Activo"),
                        ft.dropdown.Option("Inactivo"),
                    ],
                    value="Todos",
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _table_card(self) -> ft.Card:
        books = [
            ("1001", "El principito", "Antoine de Saint-Exupéry", "9780156012195", "Ficción", "Activo"),
            ("1002", "Cien años de soledad", "Gabriel García Márquez", "9780307474728", "Ficción", "Activo"),
            ("1003", "Sapiens", "Yuval Noah Harari", "9780062316097", "Historia", "Activo"),
            ("1004", "Breves respuestas...", "Stephen Hawking", "9788498388278", "Ciencia", "Activo"),
            ("1005", "Clean Code", "Robert C. Martin", "9780132350884", "Tecnología", "Inactivo"),
        ]

        rows = []
        for book_id, title, author, isbn, category, status in books:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(book_id, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(title)),
                        ft.DataCell(ft.Text(author)),
                        ft.DataCell(ft.Text(isbn)),
                        ft.DataCell(ft.Text(category)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Editar"),
                                    ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, tooltip="Detalle"),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        tooltip="Eliminar",
                                        icon_color=COLORS.DANGER,
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
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Autor")),
                ft.DataColumn(ft.Text("ISBN")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=rows,
            column_spacing=24,
            heading_row_color=COLORS.SURFACE_ALT,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=8,
        )
        return ft.Card(
            elevation=0,
            bgcolor=COLORS.SURFACE,
            content=ft.Container(
                content=ft.Row([table], scroll=ft.ScrollMode.AUTO, expand=True),
                padding=8,
                expand=True,
            ),
            expand=True,
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
