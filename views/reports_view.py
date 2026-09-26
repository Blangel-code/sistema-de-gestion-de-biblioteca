"""Vista de reportes y estadísticas de BiblioGest."""

import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import flet as ft
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config import PALETTE as COLORS
from querys import ReportData, get_export_data


class ReportsView(ft.Column):
    """Dashboard de reportes alimentado por los datos actuales de ``querys``."""

    def __init__(self) -> None:
        self.period = "Últimos 7 días"
        today = date.today()
        self.report_data: ReportData = self._report_data_for_range(
            (today - timedelta(days=6)).isoformat(),
            today.isoformat(),
        )
        self.header = self._build_header()
        self.period_filter = ft.Dropdown(
            label="Rango de fechas",
            value=self.period,
            width=190,
            options=[
                ft.dropdown.Option("Últimos 7 días"),
                ft.dropdown.Option("Este mes"),
                ft.dropdown.Option("Año actual"),
                ft.dropdown.Option("Personalizado"),
            ],
            on_select=self._change_period,
        )
        self.custom_start = ft.TextField(
            label="Desde",
            hint_text="AAAA-MM-DD",
            width=130,
            visible=False,
            on_change=self._refresh_custom_period,
        )
        self.custom_end = ft.TextField(
            label="Hasta",
            hint_text="AAAA-MM-DD",
            width=130,
            visible=False,
            on_change=self._refresh_custom_period,
        )
        self.export_menu = ft.PopupMenuButton(
            content="Exportar",
            icon=ft.Icons.DOWNLOAD_OUTLINED,
            tooltip="Exportar reporte",
            items=[
                ft.PopupMenuItem("Exportar CSV", on_click=self._export_csv),
                ft.PopupMenuItem("Exportar PDF", on_click=self._export_pdf),
            ],
        )
        super().__init__(
            controls=[
                self._toolbar(),
                self._kpi_row(),
                self._books_section(),
                self._loans_section(),
                self._users_section(),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _build_header(self) -> ft.Column:
        return ft.Column(
            [
                ft.Text("Reportes y Estadísticas", size=26, weight=ft.FontWeight.BOLD, color=COLORS.TEXT),
                ft.Text("Analiza el comportamiento de tu biblioteca", size=13, color=COLORS.TEXT_MUTED),
            ],
            spacing=3,
        )

    def _toolbar(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(expand=True),
                self.period_filter,
                self.custom_start,
                self.custom_end,
                self.export_menu,
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _open_export_menu(self, event: ft.ControlEvent) -> None:
        self.export_menu.left = event.control.left
        self.export_menu.top = event.control.top + event.control.height
        event.page.overlay.append(self.export_menu)
        self.export_menu.visible = True
        event.page.update()

    def _change_period(self, event: ft.ControlEvent) -> None:
        self.period = event.control.value or "Últimos 7 días"
        custom = self.period == "Personalizado"
        self.custom_start.visible = custom
        self.custom_end.visible = custom
        if not custom:
            self._refresh_report_data(event.page)
        event.page.update()
        self._show_message(event.page, f"Reporte actualizado: {self.period}")

    def _refresh_custom_period(self, event: ft.ControlEvent) -> None:
        if self.period != "Personalizado":
            return
        try:
            self._refresh_report_data(event.page)
        except ValueError:
            return

    def _refresh_report_data(self, page: ft.Page) -> None:
        start_date, end_date = self._selected_dates()
        self.report_data = self._report_data_for_range(start_date, end_date)
        toolbar = self.controls[0]
        self.controls = [
            toolbar,
            self._kpi_row(),
            self._books_section(),
            self._loans_section(),
            self._users_section(),
        ]
        page.update()

    def _kpi_row(self) -> ft.Row:
        cards = [
            ("Préstamos activos", self.report_data["active_loans"], "Libros actualmente fuera", ft.Icons.SWAP_HORIZ_OUTLINED, COLORS.PRIMARY),
            ("Préstamos vencidos", self.report_data["overdue_loans"], "Requieren seguimiento", ft.Icons.WARNING_AMBER_OUTLINED, COLORS.DANGER),
            ("Libros en inventario", self.report_data["inventory_books"], "Unidades registradas", ft.Icons.MENU_BOOK_OUTLINED, COLORS.SECONDARY),
            ("Usuarios registrados", self.report_data["registered_users"], "Usuarios activos", ft.Icons.GROUP_OUTLINED, COLORS.PRIMARY),
        ]
        return ft.Row([self._kpi_card(*card) for card in cards], spacing=16)

    def _kpi_card(self, title: str, value: int, detail: str, icon: str, color: str) -> ft.Container:
        return ft.Container(
            expand=True,
            padding=18,
            bgcolor=COLORS.SURFACE,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=12,
            content=ft.Column(
                [
                    ft.Row([ft.Text(title, size=12, color=COLORS.TEXT_MUTED), ft.Icon(icon, size=20, color=color)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"{value:,}", size=27, weight=ft.FontWeight.BOLD, color=COLORS.TEXT),
                    ft.Text(detail, size=11, color=COLORS.TEXT_MUTED),
                ],
                spacing=7,
            ),
        )

    def _panel(self, title: str, subtitle: str, content: ft.Control, expand: int = 1) -> ft.Container:
        return ft.Container(
            expand=expand,
            padding=18,
            bgcolor=COLORS.SURFACE,
            border=ft.Border.all(1, COLORS.BORDER),
            border_radius=12,
            content=ft.Column([ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=COLORS.TEXT), ft.Text(subtitle, size=11, color=COLORS.TEXT_MUTED), ft.Divider(height=8, color=COLORS.BORDER), content], spacing=8),
        )

    def _section_title(self, title: str) -> ft.Text:
        return ft.Text(title, size=17, weight=ft.FontWeight.BOLD, color=COLORS.TEXT)

    def _books_section(self) -> ft.Column:
        return ft.Column([self._section_title("Libros e Inventario"), ft.Row([self._top_books_panel(), self._categories_panel(), self._inactive_books_panel()], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START)], spacing=10)

    def _top_books_panel(self) -> ft.Container:
        maximum = max(value for _, value in self.report_data["top_books"])
        rows = [
            ft.Column([ft.Row([ft.Text(title, size=12, expand=True), ft.Text(str(value), size=12, weight=ft.FontWeight.BOLD)]), ft.ProgressBar(value=value / maximum, color=COLORS.PRIMARY, bgcolor=COLORS.PRIMARY_LIGHT)], spacing=4)
            for title, value in self.report_data["top_books"]
        ]
        return self._panel("Top libros prestados", "Títulos con mayor demanda", ft.Column(rows, spacing=9), expand=2)

    def _categories_panel(self) -> ft.Container:
        total = sum(value for _, value in self.report_data["categories"])
        colors = [COLORS.PRIMARY, COLORS.SECONDARY, COLORS.WARNING, ft.Colors.INDIGO_400]
        rows = [
            ft.Column([ft.Row([ft.Container(width=8, height=8, bgcolor=colors[index], border_radius=4), ft.Text(category, size=12, expand=True), ft.Text(f"{value / total:.0%}", size=12, weight=ft.FontWeight.BOLD)]), ft.ProgressBar(value=value / total, color=colors[index], bgcolor=COLORS.SURFACE_ALT)], spacing=4)
            for index, (category, value) in enumerate(self.report_data["categories"])
        ]
        return self._panel("Categorías más solicitadas", "Distribución de préstamos", ft.Column(rows, spacing=9), expand=1)

    def _inactive_books_panel(self) -> ft.Container:
        rows = [ft.Row([ft.Text(title, size=12, expand=True), ft.Text(category, size=11, color=COLORS.TEXT_MUTED)]) for title, category in self.report_data["books_without_activity"]]
        return self._panel("Libros sin movimiento", "Sin préstamos registrados", ft.Column(rows, spacing=10), expand=1)

    def _loans_section(self) -> ft.Column:
        return ft.Column([self._section_title("Préstamos y Devoluciones"), ft.Row([self._history_panel(), self._returns_panel()], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START)], spacing=10)

    def _history_panel(self) -> ft.Container:
        maximum = max(max(lent, returned) for _, lent, returned in self.report_data["monthly_history"])
        columns = [
            ft.Column([ft.Container(height=100 * lent / maximum, width=22, bgcolor=COLORS.PRIMARY, border_radius=ft.BorderRadius.only(top_left=5, top_right=5)), ft.Text(month, size=10, color=COLORS.TEXT_MUTED)], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.CENTER, height=125)
            for month, lent, _ in self.report_data["monthly_history"]
        ]
        return self._panel("Histórico mensual", "Préstamos registrados por mes", ft.Row(columns, alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END), expand=2)

    def _returns_panel(self) -> ft.Container:
        on_time = self.report_data["returns_on_time"]
        late = self.report_data["returns_late"]
        return self._panel("Devoluciones", "A tiempo vs. atrasadas", ft.Column([ft.Text(f"{on_time}%", size=30, weight=ft.FontWeight.BOLD, color=COLORS.SUCCESS), ft.ProgressBar(value=on_time / 100, color=COLORS.SUCCESS, bgcolor=COLORS.DANGER_BG), ft.Row([ft.Text("A tiempo", size=11, color=COLORS.TEXT_MUTED, expand=True), ft.Text(f"{late}% atrasadas", size=11, color=COLORS.DANGER)])], spacing=10), expand=1)

    def _users_section(self) -> ft.Column:
        return ft.Column([self._section_title("Usuarios"), ft.Row([self._readers_panel(), self._overdue_panel()], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START)], spacing=10)

    def _readers_panel(self) -> ft.Container:
        rows = [ft.Row([ft.Text(f"{index}.", size=12, color=COLORS.TEXT_MUTED, width=20), ft.Text(name, size=12, expand=True), ft.Text(f"{count} solicitudes", size=11, color=COLORS.TEXT_MUTED)]) for index, (name, count) in enumerate(self.report_data["top_readers"], 1)]
        return self._panel("Top lectores", "Usuarios con más solicitudes", ft.Column(rows, spacing=10), expand=1)

    def _overdue_panel(self) -> ft.Container:
        rows = [ft.Row([ft.Column([ft.Text(name, size=12, weight=ft.FontWeight.W_600), ft.Text(last_seen, size=11, color=COLORS.TEXT_MUTED)], expand=True, spacing=2), ft.Container(ft.Text(f"{count} vencimientos", size=11, color=COLORS.DANGER), bgcolor=COLORS.DANGER_BG, border_radius=10, padding=ft.Padding.symmetric(horizontal=8, vertical=4))]) for name, count, last_seen in self.report_data["repeat_overdue_users"]]
        return self._panel("Usuarios con múltiples vencimientos", "Seguimiento a morosos", ft.Column(rows, spacing=9), expand=2)

    def _export_csv(self, event: ft.ControlEvent) -> None:
        try:
            start_date, end_date = self._selected_dates()
            export_data = get_export_data(start_date, end_date)
            directory = self._export_directory()
            headers = {
                "Books": ["bookID", "isbn", "title", "autor", "category", "publisher", "year", "pages", "description", "stock_total", "stock_available"],
                "Users": ["userID", "name", "email", "phone", "id_card", "state", "registration_date"],
                "Orders": ["orderID", "userID", "bookID", "status", "date_lending", "date_return", "actual_return_date"],
            }
            paths = []
            for table_name, rows in export_data.items():
                path = directory / f"{table_name.lower()}.csv"
                with path.open("w", newline="", encoding="utf-8-sig") as file:
                    writer = csv.writer(file)
                    writer.writerow(headers[table_name])
                    writer.writerows(rows)
                paths.append(path)
        except ValueError as error:
            self._show_message(event.page, str(error))
            return
        self._finish_export(event, paths)

    @staticmethod
    def _report_data_for_range(start_date: str, end_date: str) -> ReportData:
        """Genera los datos del PDF únicamente con registros del periodo."""
        books, users, orders = get_export_data(start_date, end_date).values()
        book_by_id = {row[0]: row for row in books}
        user_by_id = {row[0]: row for row in users}
        book_counts = Counter(row[2] for row in orders)
        category_counts = Counter(book_by_id[row[2]][4] for row in orders)
        reader_counts = Counter(user_by_id[row[1]][1] for row in orders if row[1] in user_by_id)
        today = date.today()
        active = [row for row in orders if row[3] == "Activo"]
        overdue = [row for row in active if date.fromisoformat(row[5]) < today]
        returned = [row for row in orders if row[3] == "Devuelto" and row[6]]
        on_time = sum(date.fromisoformat(row[6]) <= date.fromisoformat(row[5]) for row in returned)
        late = len(returned) - on_time
        overdue_by_user = Counter(
            row[1]
            for row in orders
            if (row[3] == "Activo" and date.fromisoformat(row[5]) < today)
            or (row[3] == "Devuelto" and row[6] and date.fromisoformat(row[6]) > date.fromisoformat(row[5]))
        )
        last_overdue = {}
        for row in orders:
            if row[1] in overdue_by_user:
                last_overdue[row[1]] = max(last_overdue.get(row[1], row[5]), row[6] or row[5])
        repeat_overdue = [
            (
                user_by_id[user_id][1],
                count,
                f"Hace {max(0, (today - date.fromisoformat(last_overdue[user_id])).days)} días",
            )
            for user_id, count in overdue_by_user.most_common(4)
            if count > 1 and user_id in user_by_id
        ]
        months = sorted({row[4][:7] for row in orders})
        month_names = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
        monthly_history = []
        for month in months:
            lent = sum(row[4].startswith(month) for row in orders)
            returned_count = sum(row[6] and row[6].startswith(month) for row in returned)
            monthly_history.append((month_names[int(month[5:7]) - 1], lent, returned_count))
        books_without_activity = [
            (row[2], row[4]) for row in books if row[0] not in {order[2] for order in orders}
        ]
        return {
            "active_loans": len(active),
            "overdue_loans": len(overdue),
            "inventory_books": sum(row[9] or 0 for row in books),
            "registered_users": len([row for row in users if row[5] == "Activo"]),
            "top_books": [(book_by_id[book_id][2], count) for book_id, count in book_counts.most_common(5)],
            "categories": category_counts.most_common(4),
            "books_without_activity": books_without_activity,
            "monthly_history": monthly_history,
            "returns_on_time": round(100 * on_time / len(returned)) if returned else 0,
            "returns_late": round(100 * late / len(returned)) if returned else 0,
            "top_readers": reader_counts.most_common(4),
            "repeat_overdue_users": repeat_overdue,
        }

    def _export_pdf(self, event: ft.ControlEvent) -> None:
        try:
            start_date, end_date = self._selected_dates()
            report_data = self._report_data_for_range(start_date, end_date)
        except ValueError as error:
            self._show_message(event.page, str(error))
            return
        path = self._export_directory() / "reporte_bibliogest.pdf"
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1565C0"),
            alignment=TA_LEFT,
            spaceAfter=4 * mm,
        )
        section_style = ParagraphStyle(
            "ReportSection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#263238"),
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
        )
        body_style = ParagraphStyle(
            "ReportBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#546E7A"),
        )
        cell_style = ParagraphStyle(
            "ReportCell",
            parent=body_style,
            textColor=colors.HexColor("#263238"),
        )

        def paragraph(value: object, style: ParagraphStyle = cell_style) -> Paragraph:
            return Paragraph(str(value), style)

        def report_table(rows: list[list[object]], widths: list[float]) -> Table:
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3F2FD")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0D47A1")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CFD8DC")),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 7),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            return table

        story: list[object] = [
            Paragraph("BiblioGest", title_style),
            Paragraph("Reporte y estadísticas de la biblioteca", body_style),
            Paragraph(f"Periodo seleccionado: {self.period}", body_style),
            Spacer(1, 5 * mm),
            Paragraph("Indicadores clave", section_style),
            report_table(
                [
                    [paragraph("Indicador"), paragraph("Valor")],
                    [paragraph("Préstamos activos"), paragraph(report_data["active_loans"])],
                    [paragraph("Préstamos vencidos"), paragraph(report_data["overdue_loans"])],
                    [paragraph("Libros en inventario"), paragraph(report_data["inventory_books"])],
                    [paragraph("Usuarios registrados"), paragraph(report_data["registered_users"])],
                ],
                [125 * mm, 40 * mm],
            ),
            Paragraph("Libros e inventario", section_style),
            report_table(
                [[paragraph("Libro"), paragraph("Préstamos")]]
                + [[paragraph(title), paragraph(value)] for title, value in report_data["top_books"]],
                [125 * mm, 40 * mm],
            ),
            PageBreak(),
            Paragraph("Categorías más solicitadas", section_style),
            report_table(
                [[paragraph("Categoría"), paragraph("Solicitudes"), paragraph("Porcentaje")]]
                + [
                    [paragraph(category), paragraph(value), paragraph(f"{value / sum(total for _, total in report_data['categories']):.0%}")]
                    for category, value in report_data["categories"]
                ],
                [90 * mm, 35 * mm, 40 * mm],
            ),
            Paragraph("Préstamos y devoluciones", section_style),
            report_table(
                [[paragraph("Mes"), paragraph("Préstamos"), paragraph("Devoluciones")]]
                + [[paragraph(month), paragraph(lent), paragraph(returned)] for month, lent, returned in report_data["monthly_history"]],
                [90 * mm, 35 * mm, 40 * mm],
            ),
            Paragraph("Usuarios", section_style),
            report_table(
                [[paragraph("Lector"), paragraph("Solicitudes")]]
                + [[paragraph(name), paragraph(count)] for name, count in report_data["top_readers"]],
                [125 * mm, 40 * mm],
            ),
        ]
        document = SimpleDocTemplate(
            str(path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            title="BiblioGest - Reportes y Estadísticas",
            author="BiblioGest",
        )
        document.build(story)
        self._finish_export(event, [path])

    @staticmethod
    def _export_directory() -> Path:
        directory = Path(__file__).resolve().parent.parent / "data" / "exports"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _selected_dates(self) -> tuple[str, str]:
        today = date.today()
        if self.period == "Últimos 7 días":
            start = today - timedelta(days=6)
        elif self.period == "Este mes":
            start = today.replace(day=1)
        elif self.period == "Año actual":
            start = today.replace(month=1, day=1)
        else:
            try:
                start = date.fromisoformat(self.custom_start.value.strip())
                end = date.fromisoformat(self.custom_end.value.strip())
            except (AttributeError, ValueError):
                raise ValueError("Usa fechas válidas con el formato AAAA-MM-DD.")
            if start > end:
                raise ValueError("La fecha inicial no puede ser posterior a la fecha final.")
            return start.isoformat(), end.isoformat()
        return start.isoformat(), today.isoformat()

    @staticmethod
    def _finish_export(event: ft.ControlEvent, paths: list[Path]) -> None:
        names = ", ".join(path.name for path in paths)
        ReportsView._show_message(event.page, f"Archivos exportados: {names}")

    @staticmethod
    def _show_message(page: ft.Page, message: str) -> None:
        page.show_dialog(ft.SnackBar(ft.Text(message)))