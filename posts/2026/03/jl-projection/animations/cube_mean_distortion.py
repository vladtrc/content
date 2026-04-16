"""Static figure: scatter plot of original vs projected distances for the cube."""
from __future__ import annotations

from manim import DOWN, GREY_B, Scene, Text, UP

from _common import (
    cube_vertices, make_scatter_axes, mean_relative_distortion,
    nice_cube_orientation, orthographic_projection_xy, pairwise_distances,
)


class CubeMeanDistortionFigure(Scene):
    def construct(self):
        points = nice_cube_orientation(cube_vertices())
        projected = orthographic_projection_xy(points)
        original = pairwise_distances(points)
        reduced = pairwise_distances(projected)
        mean_d = mean_relative_distortion(original, reduced)

        header = Text("Куб: 3D -> 2D", font_size=28, weight="BOLD").to_edge(UP)
        subtitle = Text(f"Среднее относительное искажение: {mean_d:.1%}", font_size=18, color=GREY_B).next_to(header, DOWN, buff=0.12)
        chart = make_scatter_axes(original, reduced, "", "")
        chart.move_to(DOWN * 0.25)

        self.add(header, subtitle, chart[1])
