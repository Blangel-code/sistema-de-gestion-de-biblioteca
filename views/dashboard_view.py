"""Controles propios del encabezado del panel principal."""

import flet as ft

from config import PALETTE as COLORS


class DashboardHeader(ft.Column):
    """Título y acciones del panel, independiente del layout de navegación."""

    def __init__(self) -> None:
        super().__init__(
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
        )
