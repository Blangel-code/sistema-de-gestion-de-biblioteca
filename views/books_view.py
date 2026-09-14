"""Vista visual del catálogo de libros."""

import flet as ft

from components.modals import BookDetailsDialog, BookFormDialog, DeleteConfirmationDialog
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
                    on_click=self._open_book_dialog,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _open_book_dialog(self, event: ft.ControlEvent) -> None:
        """Abre el formulario modal para registrar un libro."""
        dialog = BookFormDialog(
            on_submit=lambda data: self._submit_book(event.page, data),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    @staticmethod
    def _submit_book(page: ft.Page, data: dict[str, str]) -> None:
        """Cierra el formulario después de recibir los datos del libro."""
        page.pop_dialog()
        

    def _filters(self) -> ft.Row:
        return ft.Row(
            controls=[
                self.search_field,
                ft.Dropdown(
                    label="Categoría",
                    width=170,
                    options=[
                        ft.dropdown.Option("Todas",style=ft.ButtonStyle(side=ft.BorderSide(color=COLORS.BORDER,width=2))),
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
            ("1001", "9780156012195", "El principito", "Antoine de Saint-Exupéry", "Ficción", "Activo", "Una historia sobre la amistad, la responsabilidad y la mirada de la infancia."),
            ("1002", "9780307474728", "Cien años de soledad", "Gabriel García Márquez", "Ficción", "Activo", "La saga de la familia Buendía a través de varias generaciones en Macondo."),
            ("1003", "9780062316097", "Sapiens", "Yuval Noah Harari", "Historia", "Activo", "Un recorrido por la evolución de la humanidad y sus grandes transformaciones."),
            ("1004", "9788498388278", "Breves respuestas...", "Stephen Hawking", "Ciencia", "Activo", "Reflexiones accesibles sobre el universo, el tiempo y el futuro de la humanidad."),
            ("1005", "9780132350884", "Clean Code", "Robert C. Martin", "Tecnología", "Inactivo", "Principios prácticos para escribir código legible, mantenible y profesional."),
        ]

        def _open_details_dialog(event: ft.ControlEvent, book: dict[str, str]) -> None:
            dialog = BookDetailsDialog(
                book=book,
                on_close=event.page.pop_dialog,
            )
            event.page.show_dialog(dialog)

        def _open_delete_dialog(event:ft.ControlEvent) -> None:
            """Abre el menú de confirmación para eliminar un registro de un libro"""
            dialog = DeleteConfirmationDialog(
                on_confirm=lambda:_delete_book(event.page),
                on_cancel=event.page.pop_dialog,
            )
            event.page.show_dialog(dialog)

        rows = []
        for book_id, isbn, title, author, category, status, description in books:
            book = {
                "isbn": isbn,
                "titulo": title,
                "autor": author,
                "categoria": category,
                "estado": status,
                "descripcion": description,
                "editorial": "Ediciones Horizonte",
                "anio": "2021",
                "paginas": "248",
            }
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(book_id, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(isbn, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(title)),
                        ft.DataCell(ft.Text(author)),
                        ft.DataCell(ft.Text(category)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Editar"),
                                    ft.IconButton(
                                        ft.Icons.VISIBILITY_OUTLINED,
                                        tooltip="Detalle",
                                        on_click=lambda event, selected_book=book: _open_details_dialog(event, selected_book),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        tooltip="Eliminar",
                                        icon_color=COLORS.DANGER,
                                        on_click=_open_delete_dialog,
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
            )

        def _delete_book(page:ft.Page):
            """Elimina un registro de un libro en la base de datos"""
            page.pop_dialog(),
            

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("ISBN")),
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Autor")),
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
