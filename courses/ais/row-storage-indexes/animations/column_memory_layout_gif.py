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
    config,
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


TABLE_CELL_W = 1.45
TABLE_CELL_H = 0.72
BASE_FLAT_CELL_W = 1.18
TABLE_Y = 2.05
FLAT_Y = -1.45
BOTTOM_SIDE_MARGIN = 0.7
HEADER_FONT_SIZE = 30
MAX_HEADER_WIDTH_FACTOR = 0.84
BASE_COLUMN_LABEL_FONT_SIZE = 28
MIN_COLUMN_LABEL_FONT_SIZE = 18


def make_cell(width: float, height: float, value: str, color, font_size: int) -> VGroup:
    rect = Rectangle(width=width - 0.04, height=height - 0.04, color=color, stroke_width=2)
    text = Text(value, font_size=font_size, weight="BOLD").move_to(rect.get_center())
    return VGroup(rect, text)


def make_header(value: str, color) -> Text:
    header = Text(value, font_size=HEADER_FONT_SIZE, color=color, weight="BOLD")
    max_width = TABLE_CELL_W * MAX_HEADER_WIDTH_FACTOR
    if header.width > max_width:
        header.scale_to_fit_width(max_width)
    return header


class ColumnMemoryLayoutGif(Scene):
    def construct(self):
        n_cols = len(HEADERS)
        n_rows = len(ROWS)
        total_flat = n_rows * n_cols
        base_flat_scale = BASE_FLAT_CELL_W / TABLE_CELL_W
        max_flat_width = config.frame_width - 2 * BOTTOM_SIDE_MARGIN
        flat_scale = min(base_flat_scale, max_flat_width / (total_flat * TABLE_CELL_W))
        flat_cell_w = TABLE_CELL_W * flat_scale
        flat_cell_h = TABLE_CELL_H * flat_scale
        label_scale = flat_scale / base_flat_scale
        column_label_font_size = max(
            MIN_COLUMN_LABEL_FONT_SIZE,
            round(BASE_COLUMN_LABEL_FONT_SIZE * label_scale),
        )

        table_x0 = -((n_cols - 1) / 2) * TABLE_CELL_W
        table_cells: dict[tuple[int, int], VGroup] = {}
        for c, header in enumerate(HEADERS):
            color = COLUMN_COLORS[header]
            x = table_x0 + c * TABLE_CELL_W
            self.add(
                make_header(header, color).move_to([x, TABLE_Y + 0.82, 0])
            )
            for r, row in enumerate(ROWS):
                y = TABLE_Y - r * TABLE_CELL_H
                cell = make_cell(TABLE_CELL_W, TABLE_CELL_H, row[c], color, 22)
                cell.move_to([x, y, 0])
                self.add(cell)
                table_cells[(r, c)] = cell

        flat_x0 = -((total_flat - 1) / 2) * flat_cell_w
        strip_frame = Rectangle(
            width=total_flat * flat_cell_w + 0.12,
            height=flat_cell_h + 0.12,
            color=GREY_D,
            stroke_width=2,
        ).move_to([0, FLAT_Y, 0])
        self.add(strip_frame)

        scale_factor = flat_scale
        flat_index = 0
        for c in range(n_cols):
            for r in range(n_rows):
                src = table_cells[(r, c)]
                target_x = flat_x0 + flat_index * flat_cell_w
                self.play(
                    src.animate.scale(scale_factor).move_to([target_x, FLAT_Y, 0]),
                    run_time=0.28,
                )
                flat_index += 1

        bracket_y = FLAT_Y - flat_cell_h / 2 - 0.36
        for c in range(n_cols):
            header = HEADERS[c]
            color = COLUMN_COLORS[header]
            first_idx = c * n_rows
            last_idx = first_idx + n_rows - 1
            left_x = flat_x0 + first_idx * flat_cell_w - flat_cell_w / 2
            right_x = flat_x0 + last_idx * flat_cell_w + flat_cell_w / 2
            center_x = (left_x + right_x) / 2
            label = Text(
                header,
                font_size=column_label_font_size,
                color=color,
                weight="BOLD",
            ).move_to(
                [center_x, bracket_y, 0]
            )
            self.play(FadeIn(label), run_time=0.25)

        self.wait(1.8)
