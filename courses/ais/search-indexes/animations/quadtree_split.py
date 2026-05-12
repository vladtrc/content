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
    Dot,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class QuadtreeSplit(Scene):
    def construct(self):
        title = Text(
            "QuadTree: рекурсивное деление на 4 квадранта",
            font=FONT,
            font_size=26,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        side = 5.4
        canvas = Rectangle(
            width=side, height=side, color=GREY_B, stroke_width=1.8,
        )
        canvas.move_to(DOWN * 0.4 + LEFT * 3.2)

        cx, cy = canvas.get_center()[0], canvas.get_center()[1]
        ox, oy = canvas.get_left()[0], canvas.get_bottom()[1]

        def at(x: float, y: float):
            return [ox + (x / 10.0) * side, oy + (y / 10.0) * side, 0]

        # Top-level split
        v_mid = Line(
            [cx, canvas.get_bottom()[1], 0],
            [cx, canvas.get_top()[1], 0],
            color=BLUE_E,
            stroke_width=2,
        )
        h_mid = Line(
            [canvas.get_left()[0], cy, 0],
            [canvas.get_right()[0], cy, 0],
            color=BLUE_E,
            stroke_width=2,
        )

        # NE has many points → split further
        ne_v = Line(
            [cx + side / 4, cy, 0],
            [cx + side / 4, canvas.get_top()[1], 0],
            color=ORANGE,
            stroke_width=2,
        )
        ne_h = Line(
            [cx, cy + side / 4, 0],
            [canvas.get_right()[0], cy + side / 4, 0],
            color=ORANGE,
            stroke_width=2,
        )

        # Points
        pts = VGroup(
            *[Dot(at(x, y), radius=0.07, color=GREEN_E) for x, y in [
                (1.5, 7.0), (3.0, 8.0),                # NW (few)
                (1.5, 2.0),                            # SW (very few)
                (7.0, 1.0), (8.5, 2.5),                # SE
                (6.2, 6.0), (7.0, 7.5), (8.4, 7.0),    # NE upper
                (6.0, 8.5), (7.5, 9.2),                # NE upper-right
            ]],
        )

        # Capacity labels
        nw_lbl = Text("NW", font=FONT, font_size=18, color=BLUE_E)
        nw_lbl.move_to(at(0.6, 9.3))
        ne_lbl = Text("NE (split)", font=FONT, font_size=18, color=ORANGE)
        ne_lbl.move_to(at(5.4, 9.3))
        sw_lbl = Text("SW", font=FONT, font_size=18, color=BLUE_E)
        sw_lbl.move_to(at(0.6, 0.5))
        se_lbl = Text("SE", font=FONT, font_size=18, color=BLUE_E)
        se_lbl.move_to(at(8.5, 0.5))

        canvas_group = VGroup(
            canvas, v_mid, h_mid, ne_v, ne_h, pts,
            nw_lbl, ne_lbl, sw_lbl, se_lbl,
        )

        # Right: tree
        tree_caption = Text("Дерево", font=FONT, font_size=20, weight="BOLD")
        tree_caption.move_to(RIGHT * 3.2 + UP * 2.5)

        root_r = Rectangle(width=2.2, height=0.5, color=BLUE_E, stroke_width=1.8)
        root_t = Text("root", font=FONT, font_size=16, color=WHITE)
        root_t.move_to(root_r)
        root_g = VGroup(root_r, root_t)
        root_g.move_to(RIGHT * 3.2 + UP * 1.8)

        # Children NW, NE, SW, SE
        def child(label: str, x: float, y: float, *, color=BLUE_E):
            r = Rectangle(width=0.9, height=0.45, color=color, stroke_width=1.5)
            t = Text(label, font=FONT, font_size=14, color=WHITE)
            t.move_to(r)
            g = VGroup(r, t)
            g.move_to(RIGHT * x + UP * y)
            return g

        nw_n = child("NW", 1.7, 0.7)
        ne_n = child("NE", 2.8, 0.7, color=ORANGE)
        sw_n = child("SW", 3.8, 0.7)
        se_n = child("SE", 4.8, 0.7)

        # NE has 4 grandchildren
        ne_nw = child("nw", 1.9, -0.4, color=ORANGE)
        ne_ne = child("ne", 2.7, -0.4, color=ORANGE)
        ne_sw = child("sw", 3.5, -0.4, color=ORANGE)
        ne_se = child("se", 4.3, -0.4, color=ORANGE)

        def conn(a, b):
            return Line(a.get_bottom(), b.get_top(), color=GREY_B, stroke_width=1.2)

        tree = VGroup(
            tree_caption, root_g,
            nw_n, ne_n, sw_n, se_n,
            ne_nw, ne_ne, ne_sw, ne_se,
            conn(root_g, nw_n), conn(root_g, ne_n),
            conn(root_g, sw_n), conn(root_g, se_n),
            conn(ne_n, ne_nw), conn(ne_n, ne_ne),
            conn(ne_n, ne_sw), conn(ne_n, ne_se),
        )

        note = Text(
            "Где плотно — делим ещё раз; пустые квадранты остаются листьями.",
            font=FONT,
            font_size=16,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        self.add(title, canvas_group, tree, note)
