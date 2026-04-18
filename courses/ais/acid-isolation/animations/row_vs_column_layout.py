from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    GREY_D,
    LEFT,
    ORANGE,
    RIGHT,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)


HEADERS = ["id", "date", "product", "country", "rev"]
NEEDED = {"country", "rev"}
COLUMN_COLORS = {
    "id": BLUE_E,
    "date": GREY_B,
    "product": GREY_B,
    "country": ORANGE,
    "rev": GREEN_E,
}
ROWS = [
    ["1", "01-10", "Laptop", "US", "12"],
    ["2", "01-10", "Phone", "DE", "8"],
    ["3", "01-11", "Laptop", "US", "12"],
]
CELL_WIDTHS = {"id": 0.55, "date": 0.95, "product": 1.05, "country": 0.9, "rev": 0.75}
ROW_HEIGHT = 0.5


class RowVsColumnLayout(Scene):
    def construct(self):
        row_panel = self.row_panel().move_to(LEFT * 3.6)
        column_panel = self.column_panel().move_to(RIGHT * 3.6)
        self.add(row_panel, column_panel)

    def panel(self, title: str) -> tuple[VGroup, RoundedRectangle]:
        frame = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=5.2,
            color=GREY_B,
        )
        label = Text(title, font_size=24, weight="BOLD").move_to(
            frame.get_top() + DOWN * 0.34
        )
        return VGroup(frame, label), frame

    def row_block(self, values: list[str], y: float) -> VGroup:
        total_width = sum(CELL_WIDTHS[h] for h in HEADERS)
        outer = Rectangle(
            width=total_width,
            height=ROW_HEIGHT,
            color=GREY_B,
            stroke_width=2.5,
        ).move_to([0, y, 0])

        group = VGroup(outer)
        left = outer.get_left()[0]
        for header in HEADERS:
            w = CELL_WIDTHS[header]
            center_x = left + w / 2
            color = COLUMN_COLORS[header] if header in NEEDED else GREY_D
            text_color = (
                COLUMN_COLORS[header] if header in NEEDED else GREY_B
            )
            value_idx = HEADERS.index(header)
            label = Text(
                values[value_idx], font_size=16, weight="BOLD", color=text_color
            ).move_to([center_x, y, 0])
            group.add(label)
            if header != HEADERS[-1]:
                divider = Line(
                    start=[left + w, y - ROW_HEIGHT / 2, 0],
                    end=[left + w, y + ROW_HEIGHT / 2, 0],
                    color=GREY_D,
                    stroke_width=1,
                )
                group.add(divider)
            # highlight needed cells with a subtle inner border
            if header in NEEDED:
                inner = Rectangle(
                    width=w - 0.04,
                    height=ROW_HEIGHT - 0.04,
                    color=color,
                    stroke_width=2,
                ).move_to([center_x, y, 0])
                group.add(inner)
            left += w
        return group

    def row_panel(self) -> VGroup:
        panel, _frame = self.panel("построчное хранение")
        total_width = sum(CELL_WIDTHS[h] for h in HEADERS)
        left = -total_width / 2
        header_group = VGroup()
        x = left
        for header in HEADERS:
            w = CELL_WIDTHS[header]
            color = COLUMN_COLORS[header] if header in NEEDED else GREY_D
            header_group.add(
                Text(header, font_size=15, color=color, weight="BOLD").move_to(
                    [x + w / 2, 1.5, 0]
                )
            )
            x += w

        rows = VGroup(
            self.row_block(ROWS[0], 0.9),
            self.row_block(ROWS[1], 0.25),
            self.row_block(ROWS[2], -0.4),
        )

        query = Text("SELECT country, rev", font_size=17, color=GREY_B).move_to(
            [0, -1.25, 0]
        )
        note = Text(
            "читает все 5 колонок", font_size=16, color=GREY_B
        ).move_to([0, -1.65, 0])
        panel.add(header_group, rows, query, note)
        return panel

    def column_strip(self, x: float, header: str) -> VGroup:
        in_proj = header in NEEDED
        color = COLUMN_COLORS[header] if in_proj else GREY_D
        text_color = COLUMN_COLORS[header] if in_proj else GREY_B
        value_color = "#FFFFFF" if in_proj else GREY_B
        w = 0.9
        cells_h = ROW_HEIGHT * len(ROWS)
        outer = Rectangle(
            width=w,
            height=cells_h,
            color=color,
            stroke_width=2.5,
        ).move_to([x, 0.25, 0])
        group = VGroup(outer)
        label = Text(header, font_size=15, color=text_color, weight="BOLD").move_to(
            [x, 1.5, 0]
        )
        group.add(label)
        top = outer.get_top()[1]
        for i, row in enumerate(ROWS):
            cy = top - ROW_HEIGHT / 2 - i * ROW_HEIGHT
            group.add(
                Text(
                    row[HEADERS.index(header)],
                    font_size=16,
                    weight="BOLD",
                    color=value_color,
                ).move_to([x, cy, 0])
            )
            if i < len(ROWS) - 1:
                group.add(
                    Line(
                        start=[x - w / 2, cy - ROW_HEIGHT / 2, 0],
                        end=[x + w / 2, cy - ROW_HEIGHT / 2, 0],
                        color=GREY_D,
                        stroke_width=1,
                    )
                )
        return group

    def column_panel(self) -> VGroup:
        panel, _frame = self.panel("поколоночное хранение")
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        strips = VGroup(
            *(self.column_strip(x, h) for x, h in zip(xs, HEADERS, strict=True))
        )

        query = Text("SELECT country, rev", font_size=17, color=GREY_B).move_to(
            [0, -1.25, 0]
        )
        note = Text(
            "читает только 2 колонки", font_size=16, color=GREY_B
        ).move_to([0, -1.65, 0])
        panel.add(strips, query, note)
        return panel
