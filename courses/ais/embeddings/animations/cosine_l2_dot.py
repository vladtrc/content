from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    LEFT,
    ORANGE,
    RIGHT,
    UP,
    WHITE,
    Arrow,
    Dot,
    DashedLine,
    Line,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class CosineL2Dot(Scene):
    def construct(self):
        title = Text(
            "Cosine vs L2 vs dot product:  длина имеет значение?",
            font=FONT,
            font_size=26,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        origin = LEFT * 1.5 + DOWN * 0.4

        # Axes
        ax_x = Line(origin + LEFT * 0.2, origin + RIGHT * 5.0, color=GREY_B, stroke_width=1.5)
        ax_y = Line(origin + DOWN * 0.2, origin + UP * 3.4, color=GREY_B, stroke_width=1.5)

        # Vectors: q points right; a_short and a_long same direction; b orthogonal
        q = Arrow(
            origin, origin + RIGHT * 2.3 + UP * 0.6,
            color=BLUE_E, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.09,
        )
        q_lbl = Text("q", font=FONT, font_size=20, color=BLUE_E)
        q_lbl.next_to(q.get_end(), UP, buff=0.05)

        a_short = Arrow(
            origin, origin + RIGHT * 1.6 + UP * 1.4,
            color=ORANGE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.10,
        )
        a_short_lbl = Text("a_short", font=FONT, font_size=18, color=ORANGE)
        a_short_lbl.next_to(a_short.get_end(), LEFT, buff=0.1)

        a_long = Arrow(
            origin, origin + RIGHT * 4.3 + UP * 3.0,
            color=ORANGE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.06,
        )
        a_long_lbl = Text("a_long (то же направление)", font=FONT, font_size=16, color=ORANGE)
        a_long_lbl.next_to(a_long.get_end(), RIGHT, buff=0.1)

        # Right: table
        rows = [
            ("Метрика", "f(q, a_short)", "f(q, a_long)"),
            ("cosine", "≈ 0.99", "≈ 0.99"),
            ("L2", "малое", "большое"),
            ("dot product", "малое", "большое"),
        ]

        def cell(text: str, *, color=WHITE):
            t = Text(text, font=FONT, font_size=16, color=color)
            return t

        table_rows = VGroup()
        for i, row in enumerate(rows):
            row_g = VGroup(
                cell(row[0], color=BLUE_E if i == 0 else WHITE),
                cell(row[1], color=BLUE_E if i == 0 else WHITE),
                cell(row[2], color=BLUE_E if i == 0 else WHITE),
            ).arrange(RIGHT, buff=0.6, aligned_edge=LEFT)
            table_rows.add(row_g)
        table_rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        table_rows.move_to(RIGHT * 3.8 + UP * 0.2)

        bottom = Text(
            "cosine инвариантен к длине;  dot product награждает длинные векторы;\n"
            "после нормализации все три метрики дают один порядок:  cos = u·v = 1 − ||u−v||²/2.",
            font=FONT,
            font_size=15,
            color=GREY_B,
        )
        bottom.to_edge(DOWN, buff=0.3)

        self.add(
            title, ax_x, ax_y,
            q, q_lbl, a_short, a_short_lbl, a_long, a_long_lbl,
            table_rows, bottom,
        )
