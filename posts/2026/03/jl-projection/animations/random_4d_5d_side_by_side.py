"""Static figure: side-by-side scatter plots for 4D->3D and 5D->4D projections."""
from __future__ import annotations

import numpy as np
from manim import DOWN, RIGHT, Scene, Text, UP, VGroup

from _common import (
    cube_vertices, make_scatter_axes, pairwise_distances,
    random_projection, scaled_random_points,
)


class Random4D5DSideBySideFigure(Scene):
    def construct(self):
        cube_median = float(np.median(pairwise_distances(cube_vertices())))
        rng4 = np.random.default_rng(7)
        rng5 = np.random.default_rng(11)

        points4 = scaled_random_points(rng4, source_dim=4, n_points=8, target_median_distance=cube_median)
        projected4 = random_projection(points4, target_dim=3, rng=rng4)
        original4, reduced4 = pairwise_distances(points4), pairwise_distances(projected4)

        points5 = scaled_random_points(rng5, source_dim=5, n_points=8, target_median_distance=cube_median)
        projected5 = random_projection(points5, target_dim=4, rng=rng5)
        original5, reduced5 = pairwise_distances(points5), pairwise_distances(projected5)

        title = Text("Два одиночных прогона подряд: 4D и 5D", font_size=30, weight="BOLD").to_edge(UP)
        left = make_scatter_axes(original4, reduced4, "4D -> 3D", "8 случайных точек")
        right = make_scatter_axes(original5, reduced5, "5D -> 4D", "Тот же размер выборки")
        panels = VGroup(left, right).arrange(RIGHT, buff=0.6).scale(0.88).move_to(DOWN * 0.2)
        self.add(title, panels)
