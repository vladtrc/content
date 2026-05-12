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
    Circle,
    Dot,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class KdtreePartitions(Scene):
    def construct(self):
        title = Text(
            "KD-tree: попеременное деление по осям X / Y",
            font=FONT,
            font_size=26,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        side_w, side_h = 6.6, 5.4
        canvas = Rectangle(
            width=side_w, height=side_h, color=GREY_B, stroke_width=1.8,
        )
        canvas.move_to(LEFT * 2.7 + DOWN * 0.4)

        ox = canvas.get_left()[0]
        oy = canvas.get_bottom()[1]

        def at(x: float, y: float):
            return [ox + (x / 10.0) * side_w, oy + (y / 10.0) * side_h, 0]

        # Points
        points = [
            ("A", 2, 3),
            ("B", 5, 4),
            ("C", 9, 6),
            ("D", 4, 7),
            ("E", 8, 1),
            ("F", 7, 2),
            ("G", 3, 9),
        ]
        dots = VGroup()
        for name, x, y in points:
            d = Dot(at(x, y), radius=0.08, color=GREEN_E)
            t = Text(name, font=FONT, font_size=14, color=GREEN_E)
            t.next_to(d, UP, buff=0.04)
            dots.add(VGroup(d, t))

        # Splits
        # B (5,4) split X=5: full height vertical line
        sx_B = Line(at(5, 0), at(5, 10), color=BLUE_E, stroke_width=2.4)
        # D (4,7) splits Y=7 on left half
        sy_D = Line(at(0, 7), at(5, 7), color=ORANGE, stroke_width=2)
        # F (7,2) splits Y=2 on right half
        sy_F = Line(at(5, 2), at(10, 2), color=ORANGE, stroke_width=2)

        canvas_group = VGroup(canvas, sx_B, sy_D, sy_F, dots)

        # Tree on the right
        def node(label: str, axis: str, *, color=BLUE_E):
            r = Rectangle(width=1.4, height=0.55, color=color, stroke_width=1.8)
            t = Text(f"{label}  [{axis}]", font=FONT, font_size=15, color=WHITE)
            t.move_to(r)
            return VGroup(r, t)

        def leaf(label: str):
            r = Rectangle(width=0.8, height=0.45, color=GREEN_E, stroke_width=1.4)
            t = Text(label, font=FONT, font_size=14, color=WHITE)
            t.move_to(r)
            return VGroup(r, t)

        root = node("B(5,4)", "X")
        d_n = node("D(4,7)", "Y", color=ORANGE)
        f_n = node("F(7,2)", "Y", color=ORANGE)
        a_l = leaf("A")
        g_l = leaf("G")
        e_l = leaf("E")
        c_l = leaf("C")

        root.move_to(RIGHT * 3.4 + UP * 2.4)
        d_n.move_to(RIGHT * 2.2 + UP * 1.2)
        f_n.move_to(RIGHT * 4.6 + UP * 1.2)
        a_l.move_to(RIGHT * 1.6 + UP * 0.0)
        g_l.move_to(RIGHT * 2.8 + UP * 0.0)
        e_l.move_to(RIGHT * 4.0 + UP * 0.0)
        c_l.move_to(RIGHT * 5.2 + UP * 0.0)

        def conn(a, b):
            return Line(a.get_bottom(), b.get_top(), color=GREY_B, stroke_width=1.2)

        tree = VGroup(
            root, d_n, f_n, a_l, g_l, e_l, c_l,
            conn(root, d_n), conn(root, f_n),
            conn(d_n, a_l), conn(d_n, g_l),
            conn(f_n, e_l), conn(f_n, c_l),
        )

        note = Text(
            "Откаты в kNN: проверяем «другую» сторону, только если она ближе текущего лучшего расстояния.",
            font=FONT,
            font_size=15,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        self.add(title, canvas_group, tree, note)
