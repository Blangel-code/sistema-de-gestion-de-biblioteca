"""Vista y componentes exclusivos del panel principal."""

import flet as ft

from config import PALETTE as COLORS


class SummaryCard(ft.Container):
    """Tarjeta de resumen visual del dashboard."""

    def __init__(self, title: str, value: str, detail: str, icon: str, color: str) -> None:
        super().__init__(
            expand=True,
            padding=20,
            bgcolor=COLORS.SURFACE,
            border_radius=12,
            border=ft.Border.all(1, COLORS.BORDER),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(title, size=13, color=COLORS.TEXT_MUTED),
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=19),
                                width=36,
                                height=36,
                                bgcolor=COLORS.SURFACE_ALT,
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
                        color=COLORS.TEXT,
                    ),
                    ft.Text(detail, size=12, color=COLORS.TEXT_MUTED),
                ],
                spacing=8,
            ),
        )


class DashboardHeader(ft.Row):
    """Título, subtítulo y acciones propias del panel principal."""

    def __init__(self) -> None:
        super().__init__(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Panel Principal",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS.TEXT,
                        ),
                        ft.Text(
                            "Resumen general de la biblioteca",
                            size=14,
                            color=COLORS.TEXT_MUTED,
                        ),
                    ],
                    spacing=5,
                    expand=True,
                ),
                ft.OutlinedButton(
                    "Registrar préstamo",
                    icon=ft.Icons.SWAP_HORIZ_OUTLINED,
                ),
                ft.ElevatedButton(
                    "Añadir libro",
                    icon=ft.Icons.MENU_BOOK_OUTLINED,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )


class DashboardView(ft.Column):
    """Composición completa del dashboard, aislada del layout de navegación."""

    def __init__(self) -> None:
        self.header = DashboardHeader()
        super().__init__(
            controls=[
                ft.Row(
                    controls=[
                        SummaryCard(
                            "Libros en catálogo",
                            "1,248",
                            "+12 este mes",
                            ft.Icons.MENU_BOOK_OUTLINED,
                            COLORS.PRIMARY,
                        ),
                        SummaryCard(
                            "Usuarios activos",
                            "356",
                            "+8 esta semana",
                            ft.Icons.GROUP_OUTLINED,
                            COLORS.SECONDARY,
                        ),
                        SummaryCard(
                            "Préstamos activos",
                            "84",
                            "6 vencen pronto",
                            ft.Icons.SWAP_HORIZ_OUTLINED,
                            COLORS.WARNING,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[self._activity_panel(), self._quick_actions_panel()],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _activity_panel(self) -> ft.Container:
        activities = [
            ("El principito", "María González", "Hoy, 10:42", COLORS.PRIMARY),
            ("Cien años de soledad", "Carlos Rodríguez", "Ayer, 16:18", COLORS.SECONDARY),
            ("Hábitos atómicos", "Ana Martínez", "Ayer, 11:05", COLORS.WARNING),
        ]
        rows = [
            ft.Row(
                controls=[
                    ft.Container(width=8, height=8, bgcolor=color, border_radius=4),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=13, weight=ft.FontWeight.W_600),
                            ft.Text(
                                f"Prestado a {user}",
                                size=12,
                                color=COLORS.TEXT_MUTED,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Text(date, size=11, color=COLORS.TEXT_SUBTLE),
                ],
                spacing=10,
            )
            for title, user, date, color in activities
        ]
        return ft.Container(
            expand=2,
            padding=20,
            bgcolor=COLORS.SURFACE,
            border_radius=12,
            border=ft.Border.all(1, COLORS.BORDER),
            content=ft.Column(
                controls=[
                    ft.Text("Actividad reciente", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Últimos movimientos registrados",
                        size=12,
                        color=COLORS.TEXT_MUTED,
                    ),
                    ft.Divider(height=12, color=COLORS.BORDER),
                    *rows,
                ],
                spacing=12,
            ),
        )

    def _quick_actions_panel(self) -> ft.Container:
        return ft.Container(
            expand=1,
            padding=20,
            bgcolor=COLORS.PRIMARY,
            border_radius=12,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Acciones rápidas",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS.SURFACE,
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
                        color=COLORS.PRIMARY_DARK,
                        bgcolor=COLORS.SURFACE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    ),
                    ft.OutlinedButton(
                        "Añadir libro",
                        icon=ft.Icons.MENU_BOOK_OUTLINED,
                        style=ft.ButtonStyle(
                            color=COLORS.SURFACE,
                            side=ft.BorderSide(1, ft.Colors.BLUE_200),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                spacing=12,
            ),
        )
