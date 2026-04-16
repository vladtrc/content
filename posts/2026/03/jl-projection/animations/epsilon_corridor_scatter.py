"""Static figure: scatter plot with epsilon corridor showing JL guarantee."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_D, DOWN, GREEN, GREY_B, ORANGE, RED, WHITE,
    Axes, Dot, Line, Polygon, Scene, Text, UP, VGroup,
)

from _common import (
    cube_vertices, pairwise_distances, random_projection,
    relative_distortion, scaled_random_points,
)


class EpsilonCorridorScatterFigure(Scene):
    def construct(self):
        rng = np.random.default_rng(5)
        eps = 0.25
        cube_median = float(np.median(pairwise_distances(cube_vertices())))

        points = scaled_random_points(rng, source_dim=32, n_points=20, target_median_distance=cube_median)
        projected = random_projection(points, target_dim=16, rng=rng)
        original = pairwise_distances(points)
        reduced = pairwise_distances(projected)
        distortion = relative_distortion(original, reduced)
        inside_mask = distortion <= eps
        inside_count = int(np.sum(inside_mask))
        total_count = int(len(distortion))

        lo = float(min(original.min(), reduced.min()))
        hi = float(max(original.max(), reduced.max()))
        padding = (hi - lo) * 0.08 if hi > lo else 0.2
        axis_min = max(0.0, lo - padding)
        axis_max = hi + padding

        axes = Axes(
            x_range=[axis_min, axis_max, max((axis_max - axis_min) / 4, 0.5)],
            y_range=[axis_min, axis_max, max((axis_max - axis_min) / 4, 0.5)],
            x_length=6.5, y_length=6.0,
            axis_config={"color": GREY_B, "include_numbers": False},
            tips=False,
        )
        corridor = Polygon(
            axes.c2p(axis_min, (1 - eps) * axis_min),
            axes.c2p(axis_min, (1 + eps) * axis_min),
            axes.c2p(axis_max, (1 + eps) * axis_max),
            axes.c2p(axis_max, (1 - eps) * axis_max),
            fill_color=ORANGE, fill_opacity=0.2, stroke_opacity=0,
        )
        diagonal = Line(axes.c2p(axis_min, axis_min), axes.c2p(axis_max, axis_max), color=WHITE, stroke_width=2)
        lower = Line(axes.c2p(axis_min, (1 - eps) * axis_min), axes.c2p(axis_max, (1 - eps) * axis_max), color=BLUE_D, stroke_width=2)
        upper = Line(axes.c2p(axis_min, (1 + eps) * axis_min), axes.c2p(axis_max, (1 + eps) * axis_max), color=BLUE_D, stroke_width=2)

        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.04, color=GREEN if ins else RED)
            for x, y, ins in zip(original, reduced, inside_mask, strict=True)
        ])

        title = Text("Что значит \"почти сохранились расстояния\"", font_size=28, weight="BOLD").to_edge(UP)
        subtitle = Text(
            f"32D -> 16D, ε = {eps:.0%}, внутри коридора {inside_count}/{total_count} пар",
            font_size=18, color=GREY_B,
        ).next_to(title, DOWN, buff=0.12)
        chart = VGroup(axes, corridor, diagonal, lower, upper, dots).move_to(DOWN * 0.2)
        self.add(title, subtitle, chart)
