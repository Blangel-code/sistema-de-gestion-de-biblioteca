from collections.abc import Callable

import flet as ft
from config import PALETTE as COLORS
from config import VALID_ROUTES
from views.books_view import BooksView
from views.dashboard_view import DashboardView
from views.loans_view import LoansView
from views.reports_view import ReportsView
from views.users_view import UsersView


LIGHT_PALETTE = {
    "BACKGROUND": ft.Colors.BLUE_GREY_50,
    "SURFACE": ft.Colors.WHITE,
    "SURFACE_ALT": ft.Colors.BLUE_GREY_50,
    "PRIMARY_LIGHT": ft.Colors.BLUE_50,
    "BORDER": ft.Colors.BLUE_GREY_100,
    "TEXT": ft.Colors.BLUE_GREY_900,
    "TEXT_MUTED": ft.Colors.BLUE_GREY_500,
    "TEXT_SUBTLE": ft.Colors.BLUE_GREY_400,
}
DARK_PALETTE = {
    "BACKGROUND": ft.Colors.BLUE_GREY_900,
    "SURFACE": ft.Colors.BLUE_GREY_800,
    "SURFACE_ALT": ft.Colors.BLUE_GREY_700,
    "PRIMARY_LIGHT": ft.Colors.BLUE_GREY_700,
    "BORDER": ft.Colors.BLUE_GREY_600,
    "TEXT": ft.Colors.BLUE_GREY_50,
    "TEXT_MUTED": ft.Colors.BLUE_GREY_300,
    "TEXT_SUBTLE": ft.Colors.BLUE_GREY_400,
}


class SidebarItem(ft.Container):
    """Elemento de navegación reutilizable para el sidebar."""

    def __init__(
        self,
        label: str,
        icon: str,
        route: str,
        on_select: Callable[[str], None],
        selected: bool = False,
    ) -> None:
        self.route = route
        self._on_select = on_select
        self._label = label
        self._icon = icon
        self._selected = selected
        super().__init__(
            content=self._build_content(),
            bgcolor=COLORS.PRIMARY_LIGHT if selected else None,
            padding=ft.Padding.symmetric(horizontal=14, vertical=11),
            border_radius=10,
            ink=True,
            on_click=self._handle_click,
        )

    def _build_content(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Icon(
                    self._icon,
                    size=20,
                    color=ft.Colors.BLUE_GREY_700
                    if not self._selected
                    else COLORS.PRIMARY,
                ),
                ft.Text(
                    self._label,
                    size=14,
                    weight=ft.FontWeight.W_600 if self._selected else ft.FontWeight.W_400,
                    color=COLORS.TEXT,
                ),
            ],
            spacing=14,
        )

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.bgcolor = COLORS.PRIMARY_LIGHT if selected else None
        self.content = self._build_content()

    def _handle_click(self, _: ft.ControlEvent) -> None:
        self._on_select(self.route)


class Sidebar(ft.Container):
    """Barra lateral con las rutas principales de la biblioteca."""

    ITEMS = (
        ("Panel Principal", ft.Icons.DASHBOARD_OUTLINED, "/"),
        ("Libros", ft.Icons.MENU_BOOK_OUTLINED, "/libros"),
        ("Usuarios", ft.Icons.GROUP_OUTLINED, "/usuarios"),
        ("Préstamos", ft.Icons.SWAP_HORIZ_OUTLINED, "/prestamos"),
        ("Reportes", ft.Icons.INSERT_CHART_OUTLINED, "/reportes"),
    )

    def __init__(
        self,
        on_navigate: Callable[[str], None],
        selected_route: str = "/",
    ) -> None:
        self._items: list[SidebarItem] = []
        self._on_navigate = on_navigate
        self._selected_route = selected_route
        super().__init__(
            width=248,
            bgcolor=COLORS.SURFACE,
            padding=ft.Padding.all(18),
            content=self._build_content(),
        )

    def _build_content(self) -> ft.Column:
        self._items = [
            SidebarItem(
                label,
                icon,
                route,
                self._handle_navigation,
                route == self._selected_route,
            )
            for label, icon, route in self.ITEMS
        ]
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.LOCAL_LIBRARY_OUTLINED,
                                color=COLORS.SURFACE,
                                size=24,
                            ),
                            width=42,
                            height=42,
                            bgcolor=COLORS.PRIMARY,
                            border_radius=12,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "BiblioGest",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLORS.TEXT,
                                ),
                                ft.Text(
                                    "Gestión de biblioteca",
                                    size=11,
                                    color=COLORS.TEXT_MUTED,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=34, color=ft.Colors.TRANSPARENT),
                ft.Text(
                    "NAVEGACIÓN",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_400,
                ),
                ft.Column(controls=self._items, spacing=5),
                ft.Container(expand=True),
                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),
                ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Text("AD", size=12, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.TEAL_600,
                            radius=18,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Administrador",
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=COLORS.TEXT,
                                ),
                                ft.Text(
                                    "Sesión activa",
                                    size=11,
                                    color=COLORS.TEXT_MUTED,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(
                            ft.Icons.MORE_HORIZ,
                            color=ft.Colors.BLUE_GREY_400,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=12,
            expand=True,
        )

    def _handle_navigation(self, route: str) -> None:
        for item in self._items:
            item.set_selected(item.route == route)
        self._on_navigate(route)


class ContentView(ft.Container):
    """Zona principal que renderiza el contenido asociado a cada ruta."""

    def __init__(self) -> None:
        self.current_route = "/"
        super().__init__(expand=True, padding=ft.Padding.all(30), content=self._build_content())

    def set_route(self, route: str) -> None:
        self.current_route = route if route in VALID_ROUTES else "/"
        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        if self.current_route == "/":
            view = DashboardView()
            header = view.header
            body = view
        elif self.current_route == "/libros":
            view = BooksView()
            header = view.header
            body = view
        elif self.current_route == "/usuarios":
            view = UsersView()
            header = view.header
            body = view
        elif self.current_route == "/prestamos":
            view = LoansView()
            header = view.header
            body = view
        elif self.current_route == "/reportes":
            view = ReportsView()
            header = view.header
            body = view
        else:
            header = ft.Column()
            body = self._placeholder_body()

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        header,
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_NONE_OUTLINED,
                            icon_color=COLORS.TEXT_SUBTLE,
                            tooltip="Notificaciones",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.HELP_OUTLINE,
                            icon_color=COLORS.TEXT_SUBTLE,
                            tooltip="Ayuda",
                            on_click=self._show_help,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(content=body, expand=True),
            ],
            expand=True,
        )

    def _show_help(self, event: ft.ControlEvent) -> None:
        help_content = {
            "/": (
                "Panel Principal",
                "Consulta un resumen del inventario, los usuarios activos, "
                "los préstamos vigentes y la actividad reciente de la biblioteca.",
            ),
            "/libros": (
                "Libros",
                "Administra el catálogo de libros. Puedes buscar por título, "
                "ISBN o autor, filtrar por categoría o estado, agregar libros, "
                "editar sus datos y controlar el inventario disponible.",
            ),
            "/usuarios": (
                "Usuarios",
                "Gestiona los usuarios registrados. Busca por nombre o cédula, "
                "filtra por estado, registra nuevos usuarios y actualiza o elimina "
                "sus datos.",
            ),
            "/prestamos": (
                "Préstamos",
                "Registra préstamos indicando el usuario, el libro y la fecha "
                "de devolución. Consulta los estados Activo, Devuelto y Retrasado; "
                "también puedes filtrar y procesar devoluciones.",
            ),
            "/reportes": (
                "Reportes",
                "Analiza los indicadores de la biblioteca. Selecciona un rango "
                "de fechas para actualizar la vista y exportar el contenido "
                "filtrado en PDF o en archivos CSV.",
            ),
        }
        title, description = help_content.get(
            self.current_route,
            ("Ayuda", "Consulta la información disponible en esta sección."),
        )
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(description, size=14),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: event.page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        event.page.show_dialog(dialog)

    def _placeholder_body(self) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=40,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, size=48, color=ft.Colors.BLUE_300),
                    ft.Text("Vista en construcción", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "La estructura visual está lista para conectar sus controles.",
                        size=14,
                        color=ft.Colors.BLUE_GREY_500,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )


class LibraryLayout(ft.Container):
    """Layout raíz: sidebar persistente, AppBar y zona de contenido."""

    def __init__(self, on_navigate: Callable[[str], None]) -> None:
        self._on_navigate = on_navigate
        self.dark_mode = False
        self.current_route = "/"
        self.content_view = ContentView()
        self.sidebar = Sidebar(on_navigate, self.current_route)
        super().__init__(
            expand=True,
            bgcolor=COLORS.BACKGROUND,
            content=self._build_root(),
        )

    def _build_root(self) -> ft.Row:
        return ft.Row(
                controls=[
                    self.sidebar,
                    ft.VerticalDivider(width=1, color=ft.Colors.BLUE_GREY_100),
                    ft.Column(
                        controls=[
                            self._build_app_bar(),
                            self.content_view,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )

    def _build_app_bar(self) -> ft.AppBar:
        return ft.AppBar(
            title=ft.Text(
                "Sistema de Gestión de Biblioteca",
                size=15,
                weight=ft.FontWeight.W_600,
                color=COLORS.TEXT,
            ),
            bgcolor=COLORS.SURFACE,
            elevation=0,
            toolbar_height=64,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LIGHT_MODE_OUTLINED
                    if self.dark_mode
                    else ft.Icons.DARK_MODE_OUTLINED,
                    icon_color=COLORS.TEXT_SUBTLE,
                    tooltip="Cambiar a modo claro"
                    if self.dark_mode
                    else "Cambiar a modo oscuro",
                    on_click=self._toggle_theme,
                ),
            ],
        )

    @staticmethod
    def _build_theme() -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=COLORS.PRIMARY,
                on_primary=ft.Colors.WHITE,
                secondary=COLORS.SECONDARY,
                on_secondary=ft.Colors.WHITE,
                surface=COLORS.SURFACE,
                on_surface=COLORS.TEXT,
                surface_container=COLORS.SURFACE,
                on_surface_variant=COLORS.TEXT_MUTED,
            ),
            font_family="Segoe UI",
            visual_density=ft.VisualDensity.COMFORTABLE,
        )

    def _toggle_theme(self, event: ft.ControlEvent) -> None:
        self.dark_mode = not self.dark_mode
        palette = DARK_PALETTE if self.dark_mode else LIGHT_PALETTE
        for name, value in palette.items():
            setattr(COLORS, name, value)
        self.bgcolor = COLORS.BACKGROUND
        self.sidebar = Sidebar(self._on_navigate, self.current_route)
        self.content_view = ContentView()
        self.content_view.set_route(self.current_route)
        self.content = self._build_root()
        event.page.theme_mode = (
            ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        )
        event.page.theme = self._build_theme()
        event.page.bgcolor = COLORS.BACKGROUND
        event.page.update()

    def set_route(self, route: str) -> None:
        self.current_route = route if route in VALID_ROUTES else "/"
        self.content_view.set_route(route)
        for item in self.sidebar._items:
            item.set_selected(item.route == self.current_route)
