from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    LEFT,
    ORANGE,
    RIGHT,
    TEAL_E,
    UP,
    WHITE,
    Arrow,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def stage(title: str, sub: str, *, color=BLUE_E) -> VGroup:
    r = RoundedRectangle(
        corner_radius=0.14,
        width=2.4,
        height=1.4,
        color=color,
        stroke_width=2.2,
    )
    t = Text(title, font=FONT, font_size=17, color=WHITE, weight="BOLD")
    s = Text(sub, font=FONT, font_size=14, color=GREY_B)
    t.move_to(r.get_center() + UP * 0.25)
    s.move_to(r.get_center() + DOWN * 0.2)
    return VGroup(r, t, s)


def arrow_between(a: VGroup, b: VGroup, label: str | None = None) -> VGroup:
    arrow = Arrow(
        a.get_right(), b.get_left(),
        color=GREY_B, stroke_width=2.4, buff=0.05,
        max_tip_length_to_length_ratio=0.12,
    )
    g = VGroup(arrow)
    if label:
        l = Text(label, font=FONT, font_size=12, color=GREY_B)
        l.next_to(arrow, UP, buff=0.06)
        g.add(l)
    return g


class HybridPipeline(Scene):
    def construct(self):
        title = Text(
            "Hybrid search: каждый индекс сужает кандидатов своим способом",
            font=FONT,
            font_size=24,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        s1 = stage("metadata", "bitmap / B-tree", color=BLUE_E)
        s2 = stage("full-text", "inverted index", color=TEAL_E)
        s3 = stage("smысл", "vector ANN", color=ORANGE)
        s4 = stage("rerank", "cross-encoder", color=GREEN_E)

        row = VGroup(s1, s2, s3, s4).arrange(RIGHT, buff=0.6)
        row.move_to(DOWN * 0.5)

        # Pipeline arrows with cardinalities
        a12 = arrow_between(s1, s2, "10M → 200k")
        a23 = arrow_between(s2, s3, "200k → 5k")
        a34 = arrow_between(s3, s4, "5k → 200")

        # Final arrow to results
        final = Text("top-20", font=FONT, font_size=16, color=GREEN_E, weight="BOLD")
        final.move_to(s4.get_right() + RIGHT * 1.2)
        arrow_final = Arrow(
            s4.get_right(), final.get_left(),
            color=GREEN_E, stroke_width=2.6, buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )

        note = Text(
            "Каждый этап режет по своему признаку. Реранкер видит только маленькую выборку и платит дорогой моделью лишь за неё.",
            font=FONT,
            font_size=14,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        # Inputs label
        inputs = Text("каталог", font=FONT, font_size=14, color=GREY_B)
        inputs.move_to(s1.get_left() + LEFT * 0.6)
        inp_arrow = Arrow(
            inputs.get_right(), s1.get_left(),
            color=GREY_B, stroke_width=2.2, buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )

        self.add(
            title, row, a12, a23, a34,
            inputs, inp_arrow, arrow_final, final,
            note,
        )
