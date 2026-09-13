"""Configuración visual compartida por toda la aplicación."""

import flet as ft


class Palette:
    """Paleta BiblioGest basada en el menú principal."""

    PRIMARY = ft.Colors.BLUE_700
    PRIMARY_DARK = ft.Colors.BLUE_800
    PRIMARY_LIGHT = ft.Colors.BLUE_50
    SECONDARY = ft.Colors.TEAL_600
    BACKGROUND = ft.Colors.BLUE_GREY_50
    SURFACE = ft.Colors.WHITE
    SURFACE_ALT = ft.Colors.BLUE_GREY_50
    BORDER = ft.Colors.BLUE_GREY_100
    TEXT = ft.Colors.BLUE_GREY_900
    TEXT_MUTED = ft.Colors.BLUE_GREY_500
    TEXT_SUBTLE = ft.Colors.BLUE_GREY_400
    SUCCESS = ft.Colors.GREEN_800
    SUCCESS_BG = ft.Colors.GREEN_50
    DANGER = ft.Colors.RED_800
    DANGER_BG = ft.Colors.RED_50
    WARNING = ft.Colors.ORANGE_700


PALETTE = Palette()

VALID_ROUTES = {"/", "/libros", "/usuarios", "/prestamos", "/reportes"}
