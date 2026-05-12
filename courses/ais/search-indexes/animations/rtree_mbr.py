from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    LEFT,
    ORANGE,
    RED_E,
    RIGHT,
    UP,
    WHITE,
    Dot,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class RtreeMbr(Scene):
    def construct(self):
        title = Text(
            "R-tree: MBR pruning — query прямоугольник режет поддеревья",
            font=FONT,
            font_size=26,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        # Canvas
        canvas_w, canvas_h = 8.0, 5.2
        canvas = Rectangle(
            width=canvas_w, height=canvas_h, color=GREY_B, stroke_width=1.5,
        )
        canvas.move_to(DOWN * 0.4)

        ox = canvas.get_left()[0]
        oy = canvas.get_bottom()[1]

        def at(x: float, y: float):
            # 0..10 → real coords inside canvas
            return [ox + (x / 10.0) * canvas_w, oy + (y / 10.0) * canvas_h, 0]

        def point(x: float, y: float, label: str, color=BLUE_E):
            d = Dot(at(x, y), radius=0.07, color=color)
            t = Text(label, font=FONT, font_size=14, color=color)
            t.next_to(d, UP, buff=0.05)
            return VGroup(d, t)

        # Group 1 (NW): A, B, C
        gA = point(1.5, 8.0, "A")
        gB = point(2.6, 7.2, "B")
        gC = point(2.0, 9.0, "C")
        mbr1 = Rectangle(
            width=(2.6 - 1.5) / 10.0 * canvas_w + 0.4,
            height=(9.0 - 7.2) / 10.0 * canvas_h + 0.4,
            color=BLUE_E,
            stroke_width=2.2,
        )
        mbr1.move_to(at((1.5 + 2.6) / 2, (7.2 + 9.0) / 2))
        mbr1_lbl = Text("MBR_1", font=FONT, font_size=14, color=BLUE_E)
        mbr1_lbl.next_to(mbr1, UP, buff=0.05)

        # Group 2 (NE): D, E
        gD = point(7.5, 8.0, "D")
        gE = point(8.5, 6.8, "E")
        mbr2 = Rectangle(
            width=(8.5 - 7.5) / 10.0 * canvas_w + 0.4,
            height=(8.0 - 6.8) / 10.0 * canvas_h + 0.4,
            color=BLUE_E,
            stroke_width=2.2,
        )
        mbr2.move_to(at((7.5 + 8.5) / 2, (6.8 + 8.0) / 2))
        mbr2_lbl = Text("MBR_2", font=FONT, font_size=14, color=BLUE_E)
        mbr2_lbl.next_to(mbr2, UP, buff=0.05)

        # Group 3 (S, will be pruned): F, G, H
        gF = point(2.0, 1.5, "F")
        gG = point(4.5, 2.0, "G")
        gH = point(7.0, 1.2, "H")
        mbr3 = Rectangle(
            width=(7.0 - 2.0) / 10.0 * canvas_w + 0.4,
            height=(2.0 - 1.2) / 10.0 * canvas_h + 0.4,
            color=GREY_B,
            stroke_width=1.8,
        )
        mbr3.move_to(at((2.0 + 7.0) / 2, (1.2 + 2.0) / 2))
        mbr3_lbl = Text("MBR_3 (пропущено)", font=FONT, font_size=14, color=GREY_B)
        mbr3_lbl.next_to(mbr3, DOWN, buff=0.05)

        # Query rectangle (crosses MBR_1 and MBR_2, NOT MBR_3)
        qx0, qy0, qx1, qy1 = 1.2, 6.0, 8.8, 9.5
        query = Rectangle(
            width=(qx1 - qx0) / 10.0 * canvas_w,
            height=(qy1 - qy0) / 10.0 * canvas_h,
            color=ORANGE,
            stroke_width=2.8,
        )
        query.move_to(at((qx0 + qx1) / 2, (qy0 + qy1) / 2))
        query_lbl = Text("query", font=FONT, font_size=16, color=ORANGE, weight="BOLD")
        query_lbl.move_to(at(qx0 + 0.5, qy1 - 0.3))

        note = Text(
            "Корень → дети: MBR_1 ∩ q ≠ ∅ → войти; MBR_2 ∩ q ≠ ∅ → войти; MBR_3 ∩ q = ∅ → пропустить.",
            font=FONT,
            font_size=16,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.25)

        self.add(
            title, canvas,
            mbr3, mbr3_lbl, gF, gG, gH,
            mbr1, mbr1_lbl, mbr2, mbr2_lbl,
            gA, gB, gC, gD, gE,
            query, query_lbl,
            note,
        )
