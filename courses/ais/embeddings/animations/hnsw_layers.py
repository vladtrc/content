from __future__ import annotations

import math
import random

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
    Dot,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def layer_panel(
    title: str,
    n_points: int,
    edges_per_node: int,
    *,
    width: float = 4.6,
    height: float = 1.8,
    seed: int = 0,
    color=BLUE_E,
) -> VGroup:
    random.seed(seed)
    rect = Rectangle(width=width, height=height, color=GREY_B, stroke_width=1.6)
    pts = []
    for _ in range(n_points):
        x = random.uniform(-width / 2 + 0.3, width / 2 - 0.3)
        y = random.uniform(-height / 2 + 0.2, height / 2 - 0.2)
        pts.append([x, y, 0])

    dots = VGroup(*[Dot(p, radius=0.06, color=color) for p in pts])

    edges = VGroup()
    for i, p in enumerate(pts):
        # nearest by distance
        dists = sorted(
            range(len(pts)),
            key=lambda j: (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2,
        )
        for j in dists[1 : 1 + edges_per_node]:
            edges.add(Line(p, pts[j], color=color, stroke_width=1.0, stroke_opacity=0.55))

    label = Text(title, font=FONT, font_size=18, color=GREY_B)
    label.next_to(rect, LEFT, buff=0.3)

    return VGroup(rect, edges, dots, label)


class HnswLayers(Scene):
    def construct(self):
        title = Text(
            "HNSW: многослойный граф навигации",
            font=FONT,
            font_size=28,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        l2 = layer_panel("L2 (entry)", n_points=4, edges_per_node=1, seed=11, color=ORANGE)
        l1 = layer_panel("L1", n_points=10, edges_per_node=2, seed=7, color=BLUE_E)
        l0 = layer_panel("L0 (все)", n_points=24, edges_per_node=3, seed=3, color=GREEN_E)

        stack = VGroup(l2, l1, l0).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        stack.move_to(DOWN * 0.4 + RIGHT * 0.5)

        # right-side note
        note_lines = [
            "Чем выше слой —",
            "тем меньше точек",
            "и тем длиннее рёбра",
            "(«магистрали»).",
            "",
            "Параметры:",
            "M — макс. соседей,",
            "efConstruction — поиск",
            "  кандидатов при вставке,",
            "efSearch — ширина",
            "  очереди при запросе.",
        ]
        notes = VGroup(*[Text(t, font=FONT, font_size=15, color=GREY_B) for t in note_lines])
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        notes.move_to(RIGHT * 5.2 + DOWN * 0.4)

        self.add(title, stack, notes)
