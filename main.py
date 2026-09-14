import flet as ft

from config import PALETTE as COLORS
from views.layout import LibraryLayout


PAGE_TITLE = "BiblioGest | Sistema de Gestión de Biblioteca"


def build_theme() -> ft.Theme:
    """Tema claro base de la aplicación."""
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=COLORS.PRIMARY,
            on_primary=ft.Colors.WHITE,
            secondary=COLORS.SECONDARY,
            on_secondary=ft.Colors.WHITE,
            surface=COLORS.SURFACE,
            on_surface=COLORS.TEXT,
        ),
        font_family="Segoe UI",
        visual_density=ft.VisualDensity.COMFORTABLE,
    )


def main(page: ft.Page) -> None:
    page.title = PAGE_TITLE
    page.theme = build_theme()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLORS.BACKGROUND
    page.padding = 0
    page.window.min_width = 960
    page.window.min_height = 640

    layout = LibraryLayout(on_navigate=page.go)

    def handle_route_change(_: ft.RouteChangeEvent) -> None:
        layout.set_route(page.route)
        page.update()

    page.on_route_change = handle_route_change
    page.on_resized = lambda _: page.update()
    page.add(layout)
    layout.set_route(page.route or "/")
    page.update()


if __name__ == "__main__":
    ft.run(main)
