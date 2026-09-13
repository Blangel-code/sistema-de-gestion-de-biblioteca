"""Vista de formulario para crear o editar libros."""

from collections.abc import Callable

import flet as ft

from config import PALETTE as COLORS


class BookFormView(ft.Container):
    """Formulario visual de libro con previsualización de portada."""

    def __init__(
        self,
        *,
        book: dict[str, str] | None = None,
        on_submit: Callable[[dict[str, str]], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
        on_image_selected: Callable[[str], None] | None = None,
    ) -> None:
        data = book or {}
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.on_image_selected = on_image_selected
        self.title_field = ft.TextField(label="Título", value=data.get("titulo", ""))
        self.author_field = ft.TextField(label="Autor", value=data.get("autor", ""))
        self.genre_field = ft.Dropdown(
            label="Género",
            value=data.get("genero"),
            options=[
                ft.dropdown.Option("Ficción"),
                ft.dropdown.Option("Historia"),
                ft.dropdown.Option("Ciencia"),
                ft.dropdown.Option("Tecnología"),
                ft.dropdown.Option("Arte"),
            ],
        )
        self.year_field = ft.TextField(
            label="Año de publicación",
            value=data.get("anio", ""),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.quantity_field = ft.TextField(
            label="Cantidad",
            value=data.get("cantidad", "1"),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.synopsis_field = ft.TextField(
            label="Sinopsis",
            value=data.get("sinopsis", ""),
            multiline=True,
            min_lines=6,
            max_lines=8,
        )
        self.preview = self._build_preview(data.get("imagen", ""))
        super().__init__(
            expand=True,
            padding=ft.Padding.all(8),
            content=ft.Column(
                [
                    self._header(),
                    ft.Row(
                        [
                            ft.Card(
                                elevation=0,
                                expand=2,
                                content=ft.Container(
                                    padding=22,
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Información del libro",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Row(
                                                [self.title_field, self.author_field],
                                                spacing=12,
                                            ),
                                            ft.Row(
                                                [self.genre_field, self.year_field, self.quantity_field],
                                                spacing=12,
                                            ),
                                            self.synopsis_field,
                                        ],
                                        spacing=14,
                                    ),
                                ),
                            ),
                            ft.Card(
                                elevation=0,
                                expand=1,
                                content=ft.Container(
                                    padding=22,
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Portada",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            self.preview,
                                            ft.OutlinedButton(
                                                "Seleccionar imagen",
                                                icon=ft.Icons.UPLOAD_FILE,
                                                on_click=self._select_image,
                                            ),
                                            ft.Text(
                                                "PNG o JPG, máximo 5 MB",
                                                size=12,
                                                color=COLORS.TEXT_MUTED,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=12,
                                    ),
                                ),
                            ),
                        ],
                        spacing=16,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

    def _header(self) -> ft.Row:
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Añadir libro", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Completa la información del nuevo libro",
                            size=13,
                            color=COLORS.TEXT_MUTED,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.TextButton("Cancelar", on_click=self._cancel),
                ft.ElevatedButton("Guardar libro", icon=ft.Icons.SAVE_OUTLINED, on_click=self._submit),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    @staticmethod
    def _build_preview(image_src: str) -> ft.Container:
        content: ft.Control
        if image_src:
            content = ft.Image(src=image_src, fit=ft.ImageFit.CONTAIN, expand=True)
        else:
            content = ft.Column(
                [
                    ft.Icon(ft.Icons.IMAGE_OUTLINED, size=52, color=COLORS.TEXT_SUBTLE),
                    ft.Text("Sin imagen", color=COLORS.TEXT_MUTED),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        return ft.Container(
            content=content,
            width=220,
            height=270,
            bgcolor=COLORS.SURFACE_ALT,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=10,
            alignment=ft.Alignment(0, 0),
        )

    def _select_image(self, _: ft.ControlEvent) -> None:
        if self.on_image_selected is not None:
            self.on_image_selected("")

    def _submit(self, _: ft.ControlEvent) -> None:
        if self.on_submit is not None:
            self.on_submit(
                {
                    "titulo": self.title_field.value or "",
                    "autor": self.author_field.value or "",
                    "genero": self.genre_field.value or "",
                    "anio": self.year_field.value or "",
                    "cantidad": self.quantity_field.value or "",
                    "sinopsis": self.synopsis_field.value or "",
                }
            )

    def _cancel(self, _: ft.ControlEvent) -> None:
        if self.on_cancel is not None:
            self.on_cancel()
