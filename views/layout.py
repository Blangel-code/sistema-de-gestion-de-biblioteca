from collections.abc import Callable

import flet as ft


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
                    else ft.Colors.BLUE_700,
                ),
                ft.Text(
                    self._label,
                    size=14,
                    weight=ft.FontWeight.W_600 if self._selected else ft.FontWeight.W_400,
                    color=ft.Colors.BLUE_GREY_900,
                ),
            ],
            spacing=14,
        )

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.bgcolor = ft.Colors.BLUE_50 if selected else None
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
            bgcolor=ft.Colors.WHITE,
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
                                color=ft.Colors.WHITE,
                                size=24,
                            ),
                            width=42,
                            height=42,
                            bgcolor=ft.Colors.BLUE_700,
                            border_radius=12,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "BiblioGest",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_GREY_900,
                                ),
                                ft.Text(
                                    "Gestión de biblioteca",
                                    size=11,
                                    color=ft.Colors.BLUE_GREY_500,
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
                                    color=ft.Colors.BLUE_GREY_900,
                                ),
                                ft.Text(
                                    "Sesión activa",
                                    size=11,
                                    color=ft.Colors.BLUE_GREY_500,
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


class SummaryCard(ft.Container):
    """Tarjeta de resumen visual; sus cifras son datos mock de la interfaz."""

    def __init__(self, title: str, value: str, detail: str, icon: str, color: str) -> None:
        super().__init__(
            expand=True,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(title, size=13, color=ft.Colors.BLUE_GREY_600),
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=19),
                                width=36,
                                height=36,
                                bgcolor=ft.Colors.BLUE_GREY_50,
                                border_radius=10,
                                alignment=ft.Alignment(0, 0),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(
                        value,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_900,
                    ),
                    ft.Text(detail, size=12, color=ft.Colors.BLUE_GREY_500),
                ],
                spacing=8,
            ),
        )


class ContentView(ft.Container):
    """Zona principal que renderiza el contenido asociado a cada ruta."""

    TITLES = {
        "/": ("Panel Principal", "Resumen general de la biblioteca"),
        "/libros": ("Libros", "Consulta y organiza el catálogo"),
        "/usuarios": ("Usuarios", "Administra los miembros registrados"),
        "/prestamos": ("Préstamos", "Controla los préstamos activos"),
        "/reportes": ("Reportes", "Indicadores y actividad reciente"),
    }

    def __init__(self) -> None:
        self.current_route = "/"
        super().__init__(expand=True, padding=ft.Padding.all(30), content=self._build_content())

    def set_route(self, route: str) -> None:
        self.current_route = route if route in self.TITLES else "/"
        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        title, subtitle = self.TITLES[self.current_route]
        if self.current_route == "/":
            body = self._dashboard_body()
        else:
            body = self._placeholder_body(title)

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    title,
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_GREY_900,
                                ),
                                ft.Text(subtitle, size=14, color=ft.Colors.BLUE_GREY_500),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_NONE_OUTLINED,
                            icon_color=ft.Colors.BLUE_GREY_600,
                            tooltip="Notificaciones",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.HELP_OUTLINE,
                            icon_color=ft.Colors.BLUE_GREY_600,
                            tooltip="Ayuda",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=28, color=ft.Colors.TRANSPARENT),
                body,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _dashboard_body(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        SummaryCard(
                            "Libros en catálogo",
                            "1,248",
                            "+12 este mes",
                            ft.Icons.MENU_BOOK_OUTLINED,
                            ft.Colors.BLUE_700,
                        ),
                        SummaryCard(
                            "Usuarios activos",
                            "356",
                            "+8 esta semana",
                            ft.Icons.GROUP_OUTLINED,
                            ft.Colors.TEAL_600,
                        ),
                        SummaryCard(
                            "Préstamos activos",
                            "84",
                            "6 vencen pronto",
                            ft.Icons.SWAP_HORIZ_OUTLINED,
                            ft.Colors.ORANGE_700,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        self._activity_panel(),
                        self._quick_actions_panel(),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=16,
        )

    def _activity_panel(self) -> ft.Container:
        activities = [
            ("El principito", "María González", "Hoy, 10:42", ft.Colors.BLUE_700),
            ("Cien años de soledad", "Carlos Rodríguez", "Ayer, 16:18", ft.Colors.TEAL_600),
            ("Hábitos atómicos", "Ana Martínez", "Ayer, 11:05", ft.Colors.ORANGE_700),
        ]
        rows = [
            ft.Row(
                controls=[
                    ft.Container(width=8, height=8, bgcolor=color, border_radius=4),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=13, weight=ft.FontWeight.W_600),
                            ft.Text(f"Prestado a {user}", size=12, color=ft.Colors.BLUE_GREY_500),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Text(date, size=11, color=ft.Colors.BLUE_GREY_400),
                ],
                spacing=10,
            )
            for title, user, date, color in activities
        ]
        return ft.Container(
            expand=2,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
            content=ft.Column(
                controls=[
                    ft.Text("Actividad reciente", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Últimos movimientos registrados", size=12, color=ft.Colors.BLUE_GREY_500),
                    ft.Divider(height=12, color=ft.Colors.BLUE_GREY_100),
                    *rows,
                ],
                spacing=12,
            ),
        )

    def _quick_actions_panel(self) -> ft.Container:
        return ft.Container(
            expand=1,
            padding=20,
            bgcolor=ft.Colors.BLUE_700,
            border_radius=12,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Acciones rápidas",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Accede a las tareas más frecuentes.",
                        size=12,
                        color=ft.Colors.BLUE_100,
                    ),
                    ft.Divider(height=12, color=ft.Colors.BLUE_400),
                    ft.FilledButton(
                        "Registrar préstamo",
                        icon=ft.Icons.ADD,
                        color=ft.Colors.BLUE_800,
                        bgcolor=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                    ft.OutlinedButton(
                        "Añadir libro",
                        icon=ft.Icons.MENU_BOOK_OUTLINED,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            side=ft.BorderSide(1, ft.Colors.BLUE_200),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                spacing=12,
            ),
        )

    def _placeholder_body(self, title: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=40,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.CONSTRUCTION_OUTLINED, size=48, color=ft.Colors.BLUE_300),
                    ft.Text(f"Vista de {title}", size=20, weight=ft.FontWeight.BOLD),
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
            bgcolor=ft.Colors.BLUE_GREY_50,
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
                                bgcolor=ft.Colors.WHITE,
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
