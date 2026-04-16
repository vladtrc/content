"""Static figure: mean distortion vs source dimensionality."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_E, DOWN, GREY_B, LEFT, RED_E,
    Axes, Dot, Line, Scene, Text, UP, VGroup,
)

from _common import (
    cube_vertices, mean_relative_distortion, pairwise_distances,
    random_projection, scaled_random_points,
)


class DistortionVsTargetDimFigure(Scene):
    def construct(self):
        rng = np.random.default_rng(19)
        source_dims = list(range(3, 33))
        trials = 80
        means = []
        cube_median = float(np.median(pairwise_distances(cube_vertices())))

        for source_dim in source_dims:
            errors = []
            for _ in range(trials):
                points = scaled_random_points(rng, source_dim=source_dim, n_points=8, target_median_distance=cube_median)
                projected = random_projection(points, target_dim=source_dim - 1, rng=rng)
                errors.append(mean_relative_distortion(pairwise_distances(points), pairwise_distances(projected)))
            means.append(float(np.mean(errors)))

        axes = Axes(
            x_range=[3, 32, 4],
            y_range=[0, max(means) * 1.15, 0.05],
            x_length=8.0, y_length=4.5,
            axis_config={"color": GREY_B, "include_numbers": False},
            tips=False,
        )
        for dim in range(4, 33, 4):
            axes.add(Text(str(dim), font_size=16).next_to(axes.c2p(dim, 0), DOWN, buff=0.15))
        for val in np.arange(0.1, max(means) * 1.15, 0.1):
            axes.add(Text(f"{val:.1f}", font_size=16).next_to(axes.c2p(3, val), LEFT, buff=0.15))

        pts = [axes.c2p(d, m) for d, m in zip(source_dims, means, strict=True)]
        segments = VGroup(*[Line(pts[i], pts[i + 1], color=RED_E, stroke_width=3) for i in range(len(pts) - 1)])
        dots = VGroup(*[Dot(p, radius=0.04, color=BLUE_E) for p in pts])

        title = Text("Если терять одну координату, высокие размерности страдают меньше", font_size=28, weight="BOLD").to_edge(UP)
        subtitle = Text("Среднее относительное искажение при случайной проекции D -> D-1", font_size=18, color=GREY_B).next_to(title, DOWN, buff=0.12)
        chart = VGroup(axes, segments, dots).move_to(DOWN * 0.25)
        self.add(title, subtitle, chart)
