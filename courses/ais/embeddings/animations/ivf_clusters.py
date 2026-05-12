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
    TEAL_E,
    UP,
    WHITE,
    Circle,
    Dot,
    Rectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


class IvfClusters(Scene):
    def construct(self):
        title = Text(
            "IVF: пространство разбито на ячейки Вороного, query сканирует только nprobe ближайших",
            font=FONT,
            font_size=22,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        canvas = Rectangle(width=10.5, height=5.6, color=GREY_B, stroke_width=1.5)
        canvas.move_to(DOWN * 0.3)
        cx, cy = canvas.get_center()[0], canvas.get_center()[1]

        # 6 centroids
        centroids_rel = [
            (-3.4, 1.4),
            (-1.0, 1.8),
            (1.8, 1.3),
            (3.6, -0.3),
            (-0.6, -1.4),
            (-3.0, -1.0),
        ]
        centroids_abs = [[cx + x, cy + y, 0] for (x, y) in centroids_rel]

        # Points around each centroid
        random.seed(13)
        cluster_points = []
        for ci, c in enumerate(centroids_abs):
            color = [GREEN_E, BLUE_E, ORANGE, TEAL_E, BLUE_E, GREEN_E][ci]
            for _ in range(14):
                p = [c[0] + random.uniform(-0.75, 0.75), c[1] + random.uniform(-0.55, 0.55), 0]
                cluster_points.append((p, color))

        all_dots = VGroup(*[Dot(p, radius=0.05, color=col) for (p, col) in cluster_points])

        # Centroid markers
        centroids_dots = VGroup(
            *[Dot(c, radius=0.13, color=RED_E) for c in centroids_abs],
        )
        centroid_labels = VGroup(
            *[
                Text(f"c{i}", font=FONT, font_size=14, color=RED_E).next_to(centroids_dots[i], UP, buff=0.06)
                for i in range(len(centroids_abs))
            ]
        )

        # query
        q = Dot([cx + 0.4, cy + 1.2, 0], radius=0.14, color=ORANGE)
        q_lbl = Text("query", font=FONT, font_size=16, color=ORANGE, weight="BOLD")
        q_lbl.next_to(q, UP, buff=0.06)

        # nprobe = 2: highlight c1 and c2 (closest)
        ring1 = Circle(radius=0.95, color=ORANGE, stroke_width=2.4).move_to(centroids_abs[1])
        ring2 = Circle(radius=0.95, color=ORANGE, stroke_width=2.4).move_to(centroids_abs[2])

        note = Text(
            "nprobe=2: вместо N сравнений делаем сравнения только с 2 кластерами. "
            "PQ дополнительно сжимает векторы (8 бит на под-вектор).",
            font=FONT,
            font_size=15,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.3)

        self.add(
            title, canvas, all_dots, centroids_dots, centroid_labels,
            ring1, ring2, q, q_lbl, note,
        )
