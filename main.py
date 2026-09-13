import flet as ft

from views.layout import LibraryLayout


PAGE_TITLE = "BiblioGest | Sistema de Gestión de Biblioteca"


def build_theme() -> ft.Theme:
    """Tema claro base de la aplicación."""
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_700,
            on_primary=ft.Colors.WHITE,
            secondary=ft.Colors.TEAL_600,
            on_secondary=ft.Colors.WHITE,
            surface=ft.Colors.WHITE,
            on_surface=ft.Colors.BLUE_GREY_900,
        ),
        font_family="Segoe UI",
        visual_density=ft.VisualDensity.COMFORTABLE,
    )


def main(page: ft.Page) -> None:
    page.title = PAGE_TITLE
    page.theme = build_theme()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
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
    page.go(page.route or "/")


if __name__ == "__main__":
    ft.run(main)
