from collections.abc import Callable

import flet as ft
from config import PALETTE as COLORS
from config import VALID_ROUTES
from views.books_view import BooksView
from views.dashboard_view import DashboardView
from views.loans_view import LoansView
from views.users_view import UsersView


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

    def __init__(self, on_navigate: Callable[[str], None]) -> None:
        self._items: list[SidebarItem] = []
        self._on_navigate = on_navigate
        super().__init__(
            width=248,
            bgcolor=COLORS.SURFACE,
            padding=ft.Padding.all(18),
            content=self._build_content(),
        )

    def _build_content(self) -> ft.Column:
        self._items = [
            SidebarItem(label, icon, route, self._handle_navigation, route == "/")
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
        self.content_view = ContentView()
        self.sidebar = Sidebar(on_navigate)
        super().__init__(
            expand=True,
            bgcolor=COLORS.BACKGROUND,
            content=ft.Row(
                controls=[
                    self.sidebar,
                    ft.VerticalDivider(width=1, color=ft.Colors.BLUE_GREY_100),
                    ft.Column(
                        controls=[
                            ft.AppBar(
                                title=ft.Text(
                                    "Sistema de Gestión de Biblioteca",
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLUE_GREY_800,
                                ),
                                bgcolor=COLORS.SURFACE,
                                elevation=0,
                                toolbar_height=64,
                            ),
                            self.content_view,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        )

    def set_route(self, route: str) -> None:
        self.content_view.set_route(route)
