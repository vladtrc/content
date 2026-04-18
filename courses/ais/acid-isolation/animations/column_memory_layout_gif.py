from __future__ import annotations

from manim import (
    BLUE_E,
    GREEN_E,
    GREY_B,
    GREY_D,
    ORANGE,
    PURPLE_E,
    YELLOW_E,
    FadeIn,
    Indicate,
    Rectangle,
    Scene,
    Text,
    VGroup,
)


HEADERS = ["id", "date", "product", "country", "rev"]
COLUMN_COLORS = {
    "id": BLUE_E,
    "date": PURPLE_E,
    "product": YELLOW_E,
    "country": ORANGE,
    "rev": GREEN_E,
}
ROWS = [
    ["1", "01-10", "Laptop", "US", "12"],
    ["2", "01-10", "Phone", "DE", "8"],
    ["3", "01-11", "Laptop", "US", "12"],
]


TABLE_CELL_W = 1.0
TABLE_CELL_H = 0.5
FLAT_CELL_W = 0.82
FLAT_CELL_H = 0.5
TABLE_Y = 2.4
FLAT_Y = -2.0


def make_cell(width: float, height: float, value: str, color, font_size: int) -> VGroup:
    rect = Rectangle(width=width - 0.04, height=height - 0.04, color=color, stroke_width=2)
    text = Text(value, font_size=font_size, weight="BOLD").move_to(rect.get_center())
    return VGroup(rect, text)


class ColumnMemoryLayoutGif(Scene):
    def construct(self):
        n_cols = len(HEADERS)
        n_rows = len(ROWS)

        table_x0 = -((n_cols - 1) / 2) * TABLE_CELL_W
        table_cells: dict[tuple[int, int], VGroup] = {}
        for c, header in enumerate(HEADERS):
            color = COLUMN_COLORS[header]
            x = table_x0 + c * TABLE_CELL_W
            self.add(
                Text(header, font_size=16, color=color, weight="BOLD").move_to(
                    [x, TABLE_Y + 0.55, 0]
                )
            )
            for r, row in enumerate(ROWS):
                y = TABLE_Y - r * TABLE_CELL_H
                cell = make_cell(TABLE_CELL_W, TABLE_CELL_H, row[c], color, 14)
                cell.move_to([x, y, 0])
                self.add(cell)
                table_cells[(r, c)] = cell

        title = Text(
            "поколоночно в памяти", font_size=22, weight="BOLD", color=GREY_B
        ).move_to([0, 0.7, 0])
        self.add(title)

        total_flat = n_rows * n_cols
        flat_x0 = -((total_flat - 1) / 2) * FLAT_CELL_W
        strip_frame = Rectangle(
            width=total_flat * FLAT_CELL_W + 0.12,
            height=FLAT_CELL_H + 0.12,
            color=GREY_D,
            stroke_width=1.5,
        ).move_to([0, FLAT_Y, 0])
        self.add(strip_frame)

        scale_factor = FLAT_CELL_W / TABLE_CELL_W
        flat_index = 0
        for c in range(n_cols):
            for r in range(n_rows):
                src = table_cells[(r, c)]
                target_x = flat_x0 + flat_index * FLAT_CELL_W
                self.play(
                    src.animate.scale(scale_factor).move_to([target_x, FLAT_Y, 0]),
                    run_time=0.28,
                )
                flat_index += 1

        bracket_y = FLAT_Y - 0.55
        for c in range(n_cols):
            header = HEADERS[c]
            color = COLUMN_COLORS[header]
            first_idx = c * n_rows
            last_idx = first_idx + n_rows - 1
            left_x = flat_x0 + first_idx * FLAT_CELL_W - FLAT_CELL_W / 2
            right_x = flat_x0 + last_idx * FLAT_CELL_W + FLAT_CELL_W / 2
            center_x = (left_x + right_x) / 2
            label = Text(header, font_size=14, color=color, weight="BOLD").move_to(
                [center_x, bracket_y, 0]
            )
            self.play(FadeIn(label), run_time=0.25)

        self.wait(1.8)
