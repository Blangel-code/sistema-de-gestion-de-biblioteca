"""Vista visual del catálogo de libros."""

import flet as ft

from components.modals import BookDetailsDialog, BookFormDialog, DeleteConfirmationDialog
from config import PALETTE as COLORS
from querys import (
    add_book,
    eliminate_book,
    search_books,
    search_filter_of_books,
    update_book,
)

class BooksView(ft.Container):
    """Catálogo con búsqueda, filtros y acciones por libro."""

    def __init__(self) -> None:
        self.header = self._header()
        self.search_field = ft.TextField(
            hint_text="Buscar por título, autor o ISBN",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=8,
            on_change=self._refresh_table
        )
        self.category_dropdown = None
        self.status_dropdown = ft.Dropdown(
                    label="Estado",
                    width=150,
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Activo"),
                        ft.dropdown.Option("Inactivo"),
                    ],
                    value="Todos",
                    on_select=self._refresh_table,
                )
        self.table_card = ft.Container(self._table_card(), expand=True)
        super().__init__(
            expand=True,
            content=ft.Column(
                controls=[
                    self._filters(),
                    self.table_card,
                ],
                spacing=16,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
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
        self.dialog = BookFormDialog(
            on_submit=lambda data: self._submit_book(event.page, data),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(self.dialog)

    def _refresh_table(self) -> None:
        """Refresca La Tabla De Los Libros Cada Vez Que Se Llama"""
        self.table_card.content = self._table_card()
        self.page.update()

    def _delete_book(self,page:ft.Page,id_delete_book:int) -> None:
        """Elimina un registro de un libro en la base de datos"""
        success, msg = eliminate_book(id_delete_book)
        page.show_dialog(ft.SnackBar(msg))
        if not success:
            return
        self.dialog_delete.open = False
        self._refresh_table()
        page.pop_dialog()

    def _submit_book(self,page: ft.Page, data: dict[str, str]) -> None:
        """Cierra el formulario después de recibir los datos del libro."""
        success, msg = add_book(data)
        page.show_dialog(ft.SnackBar(msg))
        if not success:
            return
        self.dialog.open = False
        self._refresh_table()

    def _open_edit_dialog(self, event: ft.ControlEvent, book: dict[str, str]) -> None:
        """Abre el formulario reutilizado para editar el libro seleccionado."""
        self.dialog_edit = BookFormDialog(
            title="Editar libro",
            initial_data=book,
            on_submit=lambda data: self._submit_edit_book(event.page, book["book_id"], data),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(self.dialog_edit)

    def _submit_edit_book(
        self,
        page: ft.Page,
        book_id: int,
        data: dict[str, str],
    ) -> None:
        """Guarda la edición validada y mantiene abierto el diálogo si falla."""
        success, msg = update_book(book_id, data)
        page.show_dialog(ft.SnackBar(msg))
        if not success:
            return
        self.dialog_edit.open = False
        self._refresh_table()

    @staticmethod
    def _open_details_dialog(event: ft.ControlEvent, book: dict[str, str]) -> None:
        """Abre El Menú De Detalles Del Libro Correspondiente"""
        dialog = BookDetailsDialog(
            book=book,
            on_close=event.page.pop_dialog,
        )
        event.page.show_dialog(dialog)

    def _open_delete_dialog(self,event:ft.ControlEvent,delete_book: dict[str, str]) -> None:
        """Abre el menú de confirmación para eliminar un registro de un libro"""
        self.dialog_delete = DeleteConfirmationDialog(
            item_name=delete_book["titulo"],
            on_confirm=lambda:self._delete_book(event.page,delete_book["book_id"]),
            on_cancel=event.page.pop_dialog,
        )
        event.page.show_dialog(self.dialog_delete)

    def _filters(self) -> ft.Row:
        """Devuelve Los Filtros Disponibles. 2 Dropdown, Uno Para Seleccionar Categoría Y El Otro Para Seleccionar El Estado"""
        category_options = search_filter_of_books()
        self.category_dropdown = ft.Dropdown(
            label="Categoría",
            width=170,
            options=[
                ft.dropdown.Option("Todas",style=ft.ButtonStyle(side=ft.BorderSide(color=COLORS.BORDER,width=2))),
                *[ft.dropdown.Option(label,style=ft.ButtonStyle(side=ft.BorderSide(color=COLORS.BORDER,width=2))) for label in category_options]
            ],
            value="Todas",
            on_select=self._refresh_table,
        )
        return ft.ResponsiveRow(
            controls=[
                ft.Container(self.search_field, col={"xs": 12, "md": 8}),
                ft.Container(self.category_dropdown, col={"xs": 6, "md": 2}),
                ft.Container(self.status_dropdown, col={"xs": 6, "md": 2}),
            ],
            spacing=12,
        )

    def _table_card(self) -> ft.Card:
        books = search_books(self.status_dropdown.value if self.status_dropdown else None,self.category_dropdown.value if self.category_dropdown else None,self.search_field.value)

        rows = []
        for book_id, isbn, title, author, status, category, publisher, year, pages, description, stock_total, stock_available in books:
            book = {
                "book_id" : book_id,
                "isbn": isbn,
                "titulo": title,
                "autor": author,
                "categoria": category,
                "estado": status,
                "descripcion": description,
                "editorial": publisher,
                "anio": year,
                "paginas": pages,
                "totales": stock_total,
                "disponibles": stock_available,
            }
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(book_id, weight=ft.FontWeight.BOLD,)),
                        ft.DataCell(ft.Text(isbn, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(title,no_wrap=True,width=200,overflow=ft.TextOverflow.ELLIPSIS)),
                        ft.DataCell(ft.Text(author)),
                        ft.DataCell(ft.Text(category)),
                        ft.DataCell(self._status_badge(status)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.Icons.EDIT_OUTLINED,
                                        tooltip="Editar",
                                        on_click=lambda event, selected_book=book: self._open_edit_dialog(
                                            event,
                                            selected_book,
                                        ),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.VISIBILITY_OUTLINED,
                                        tooltip="Detalle",
                                        on_click=lambda event, selected_book=book: self._open_details_dialog(event, selected_book),
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        tooltip="Eliminar",
                                        icon_color=COLORS.DANGER,
                                        on_click=lambda event, delete_book=book: self._open_delete_dialog(event,delete_book),
                                    ),
                                ],
                                spacing=0,
                            )
                        )
                    ]
                )
            )

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
            expand=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row([table], scroll=ft.ScrollMode.AUTO),
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=0,
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