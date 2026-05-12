from __future__ import annotations

import random

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
    DashedLine,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class LshBuckets(Scene):
    def construct(self):
        title = Text(
            "LSH: случайные гиперплоскости делят пространство на бакеты",
            font=FONT,
            font_size=24,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        # Left canvas with points + 2 hyperplanes
        size = 5.0
        canvas = Rectangle(width=size, height=size, color=GREY_B, stroke_width=1.6)
        canvas.move_to(LEFT * 3.2 + DOWN * 0.3)

        cx, cy = canvas.get_center()[0], canvas.get_center()[1]

        # Two hyperplanes
        # Plane 1: slope +0.6
        p1a = [cx - size / 2, cy + size / 2 * 0.6, 0]
        p1b = [cx + size / 2, cy - size / 2 * 0.6, 0]
        plane1 = DashedLine(p1a, p1b, color=BLUE_E, stroke_width=2)

        # Plane 2: slope -1.0
        p2a = [cx - size / 2 * 0.6, cy + size / 2, 0]
        p2b = [cx + size / 2 * 0.6, cy - size / 2, 0]
        plane2 = DashedLine(p2a, p2b, color=ORANGE, stroke_width=2)

        random.seed(5)
        # Cluster A — top-left, in bucket [1, 1]
        cluster_a = [
            [cx - 1.3 + random.uniform(-0.3, 0.3), cy + 1.4 + random.uniform(-0.3, 0.3), 0]
            for _ in range(6)
        ]
        # Cluster B — center-right, in bucket [1, 0]
        cluster_b = [
            [cx + 1.4 + random.uniform(-0.3, 0.3), cy + 0.2 + random.uniform(-0.3, 0.3), 0]
            for _ in range(5)
        ]
        # Cluster C — bottom, in bucket [0, 0]
        cluster_c = [
            [cx - 0.4 + random.uniform(-0.3, 0.3), cy - 1.7 + random.uniform(-0.3, 0.3), 0]
            for _ in range(5)
        ]

        dots_a = VGroup(*[Dot(p, radius=0.08, color=GREEN_E) for p in cluster_a])
        dots_b = VGroup(*[Dot(p, radius=0.08, color=BLUE_E) for p in cluster_b])
        dots_c = VGroup(*[Dot(p, radius=0.08, color=ORANGE) for p in cluster_c])

        # Query — somewhere close to cluster_a
        q = Dot([cx - 1.4, cy + 1.3, 0], radius=0.13, color=RED_E)
        q_lbl = Text("query", font=FONT, font_size=14, color=RED_E, weight="BOLD")
        q_lbl.next_to(q, UP, buff=0.05)

        canvas_group = VGroup(canvas, plane1, plane2, dots_a, dots_b, dots_c, q, q_lbl)

        # Right: bucket list
        right_caption = Text("Таблица бакетов", font=FONT, font_size=20, weight="BOLD")
        right_caption.move_to(RIGHT * 3.4 + UP * 2.3)

        def bucket_row(code: str, items: str, *, highlight=False):
            r = RoundedRectangle(
                corner_radius=0.1, width=4.8, height=0.55,
                color=RED_E if highlight else GREY_B,
                stroke_width=2.2 if highlight else 1.4,
            )
            t_code = Text(code, font=FONT, font_size=16, color=BLUE_E if not highlight else RED_E)
            t_items = Text(items, font=FONT, font_size=15, color=WHITE)
            t_code.move_to(r.get_left() + RIGHT * 0.7)
            t_items.move_to(r.get_left() + RIGHT * 2.6)
            return VGroup(r, t_code, t_items)

        b1 = bucket_row("[1,1]", "A-cluster (6 точек) + query", highlight=True)
        b2 = bucket_row("[1,0]", "B-cluster (5 точек)")
        b3 = bucket_row("[0,1]", "—")
        b4 = bucket_row("[0,0]", "C-cluster (5 точек)")

        buckets = VGroup(b1, b2, b3, b4).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        buckets.move_to(RIGHT * 3.4 + DOWN * 0.2)

        note = Text(
            "Поиск идёт только внутри bucket-а query. С L таблиц вероятность пропуска падает экспоненциально.",
            font=FONT,
            font_size=14,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        self.add(title, canvas_group, right_caption, buckets, note)
