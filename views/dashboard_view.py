"""Vista y componentes exclusivos del panel principal."""

import flet as ft

from config import PALETTE as COLORS
from querys import get_dashboard_data


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
    """Título y subtítulo del panel principal."""

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
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )


class DashboardView(ft.Column):
    """Composición completa del dashboard, aislada del layout de navegación."""

    def __init__(self) -> None:
        self.dashboard_data = get_dashboard_data()
        self.header = DashboardHeader()
        super().__init__(
            controls=[
                ft.Row(
                    controls=[
                        SummaryCard(
                            "Libros en catálogo",
                            f"{self.dashboard_data['inventory_books']:,}",
                            "Unidades registradas en inventario",
                            ft.Icons.MENU_BOOK_OUTLINED,
                            COLORS.PRIMARY,
                        ),
                        SummaryCard(
                            "Usuarios activos",
                            f"{self.dashboard_data['active_users']:,}",
                            "Usuarios registrados activos",
                            ft.Icons.GROUP_OUTLINED,
                            COLORS.SECONDARY,
                        ),
                        SummaryCard(
                            "Préstamos activos",
                            f"{self.dashboard_data['active_loans']:,}",
                            f"{self.dashboard_data['overdue_loans']:,} vencidos",
                            ft.Icons.SWAP_HORIZ_OUTLINED,
                            COLORS.WARNING,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        self._activity_panel(),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _activity_panel(self) -> ft.Container:
        activities = self.dashboard_data["activity"]
        colors_by_status = {
            "Activo": COLORS.PRIMARY,
            "Devuelto": COLORS.SECONDARY,
            "Retrasado": COLORS.WARNING,
        }
        rows = [
            ft.Row(
                controls=[
                    ft.Container(width=8, height=8, bgcolor=color, border_radius=4),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=13, weight=ft.FontWeight.W_600),
                            ft.Text(
                                f"Préstamo de {user} · {status}",
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
            for title, user, date, status in activities
            for color in [colors_by_status.get(status, COLORS.PRIMARY)]
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
