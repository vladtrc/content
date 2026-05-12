from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    GREY_E,
    LEFT,
    ORANGE,
    RIGHT,
    UP,
    WHITE,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def bit_row(label: str, bits: list[int], *, color=BLUE_E, label_color=WHITE) -> VGroup:
    cell_w = 0.5
    cells = VGroup()
    for i, b in enumerate(bits):
        rect = Rectangle(
            width=cell_w,
            height=cell_w,
            color=color,
            fill_color=color if b else GREY_E,
            fill_opacity=0.85 if b else 0.25,
            stroke_width=1.4,
        )
        txt = Text(str(b), font=FONT, font_size=18, color=WHITE if b else GREY_B)
        txt.move_to(rect)
        rect.move_to([cell_w * i, 0, 0])
        txt.move_to(rect)
        cells.add(VGroup(rect, txt))
    cells.arrange(RIGHT, buff=0.04)
    lbl = Text(label, font=FONT, font_size=20, color=label_color)
    lbl.next_to(cells, LEFT, buff=0.35)
    return VGroup(lbl, cells)


class BitmapAnd(Scene):
    def construct(self):
        # rows for 12 строк таблицы
        paid     = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
        country  = [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0]
        result   = [a & b for a, b in zip(paid, country)]

        title = Text(
            "Bitmap: AND по двум фильтрам",
            font=FONT,
            font_size=30,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        r1 = bit_row("status = paid ", paid, color=ORANGE)
        r2 = bit_row("country = RU  ", country, color=BLUE_E)
        r3 = bit_row("AND результат ", result, color=GREEN_E)

        rows = VGroup(r1, r2, r3).arrange(DOWN, buff=0.55, aligned_edge=RIGHT)
        rows.move_to(DOWN * 0.2)

        and_line = Line(
            r2[1].get_corner(DOWN + LEFT) + DOWN * 0.15,
            r2[1].get_corner(DOWN + RIGHT) + DOWN * 0.15,
            color=GREY_B,
            stroke_width=2,
        )
        and_label = Text("AND", font=FONT, font_size=20, color=GREY_B)
        and_label.next_to(and_line, LEFT, buff=0.25)

        note = Text(
            "Один проход 64 битов за такт CPU — на миллионах строк выигрыш на порядки.",
            font=FONT,
            font_size=18,
            color=GREY_B,
        )
        note.next_to(rows, DOWN, buff=0.5)

        self.add(title, rows, and_line, and_label, note)
