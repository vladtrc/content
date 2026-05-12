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
    Circle,
    Dot,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def card(label: str, *, color=BLUE_E, width: float = 2.4) -> VGroup:
    r = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=0.7,
        color=color,
        stroke_width=2,
    )
    t = Text(label, font=FONT, font_size=18, color=WHITE)
    t.move_to(r)
    return VGroup(r, t)


class EmbeddingPipeline(Scene):
    def construct(self):
        title = Text(
            "Embedding pipeline: объекты → модель → точки в пространстве",
            font=FONT,
            font_size=26,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        # Left: objects (text, image, item)
        obj1 = card("«как вернуть товар»", color=TEAL_E)
        obj2 = card("«laptop sale»", color=TEAL_E)
        obj3 = card("товар #42", color=ORANGE)
        obj4 = card("фото кошки", color=GREEN_E)
        objs = VGroup(obj1, obj2, obj3, obj4).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        objs.move_to(LEFT * 4.3 + DOWN * 0.2)

        # Middle: model
        model = RoundedRectangle(
            corner_radius=0.18,
            width=2.2,
            height=2.8,
            color=BLUE_E,
            stroke_width=2.4,
        )
        model_t = Text("model", font=FONT, font_size=22, color=WHITE, weight="BOLD")
        model_sub = Text(
            "sentence-trans /\nBERT / CLIP",
            font=FONT,
            font_size=14,
            color=GREY_B,
        )
        model_t.move_to(model.get_center() + UP * 0.3)
        model_sub.move_to(model.get_center() + DOWN * 0.4)
        model_g = VGroup(model, model_t, model_sub)
        model_g.move_to(LEFT * 0.5 + DOWN * 0.2)

        # Arrows from objs to model
        arrows = VGroup()
        for o in objs:
            a = Arrow(
                o.get_right(),
                model.get_left() + UP * (o.get_center()[1] - model.get_center()[1]) * 0.3,
                color=GREY_B,
                stroke_width=2,
                buff=0.12,
                max_tip_length_to_length_ratio=0.1,
            )
            arrows.add(a)

        # Right: vector space (2D projection of points)
        space = Rectangle(width=4.2, height=3.6, color=GREY_B, stroke_width=1.5)
        space.move_to(RIGHT * 3.8 + DOWN * 0.2)

        sx, sy = space.get_center()[0], space.get_center()[1]

        def at(dx, dy):
            return [sx + dx, sy + dy, 0]

        # close pair (text "как вернуть товар" ~ "laptop sale" actually they're far -> use similar concept; show two close cyan and two far)
        p1 = Dot(at(-1.2, 0.8), radius=0.1, color=TEAL_E)
        p2 = Dot(at(-0.9, 0.6), radius=0.1, color=TEAL_E)
        p3 = Dot(at(0.6, -0.7), radius=0.1, color=ORANGE)
        p4 = Dot(at(1.2, 1.0), radius=0.1, color=GREEN_E)

        p1_t = Text("u₁", font=FONT, font_size=14, color=TEAL_E)
        p1_t.next_to(p1, UP, buff=0.05)
        p2_t = Text("u₂", font=FONT, font_size=14, color=TEAL_E)
        p2_t.next_to(p2, DOWN, buff=0.05)
        p3_t = Text("v_item", font=FONT, font_size=14, color=ORANGE)
        p3_t.next_to(p3, DOWN, buff=0.05)
        p4_t = Text("v_img", font=FONT, font_size=14, color=GREEN_E)
        p4_t.next_to(p4, UP, buff=0.05)

        # Arrow from model to space
        big_arrow = Arrow(
            model.get_right(),
            space.get_left(),
            color=GREY_B,
            stroke_width=2,
            buff=0.15,
            max_tip_length_to_length_ratio=0.08,
        )

        space_lbl = Text("R^d", font=FONT, font_size=18, color=GREY_B)
        space_lbl.next_to(space, UP, buff=0.1)

        space_group = VGroup(
            space, space_lbl, p1, p2, p3, p4, p1_t, p2_t, p3_t, p4_t,
        )

        note = Text(
            "Близкие по смыслу объекты получают близкие векторы.",
            font=FONT,
            font_size=17,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        self.add(title, objs, arrows, model_g, big_arrow, space_group, note)
