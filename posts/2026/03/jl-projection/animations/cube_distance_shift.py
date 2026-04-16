"""Static figure: heatmap of pairwise distance distortion after cube projection."""
from __future__ import annotations

import numpy as np
from manim import (
    DOWN, GREEN, GREEN_D, RED, RED_E, RIGHT, UP, WHITE,
    Rectangle, Scene, Text, VGroup, interpolate_color,
)

from _common import cube_vertices, nice_cube_orientation, orthographic_projection_xy, point_labels


class CubeDistanceShiftFigure(Scene):
    def construct(self):
        title = Text("Расстояния до и после проекции куба", font_size=30, weight="BOLD").to_edge(UP)

        points = nice_cube_orientation(cube_vertices())
        projected = orthographic_projection_xy(points)
        labels = point_labels()
        n = len(labels)

        d3 = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
        d2 = np.linalg.norm(projected[:, None, :] - projected[None, :, :], axis=-1)
        baseline = np.where(d3 == 0, 1.0, d3)
        distortion = np.abs(d2 - d3) / baseline
        vmax = float(max(np.max(distortion), 1e-6))

        grid = VGroup()
        cell_size = 0.6
        origin_x = -2.0
        origin_y = 2.2

        for column, label in enumerate(labels[1:]):
            grid.add(Text(label, font_size=18, weight="BOLD").move_to([origin_x + column * cell_size, origin_y + 0.45, 0]))
        for row, label in enumerate(labels[:-1]):
            grid.add(Text(label, font_size=18, weight="BOLD").move_to([origin_x - 0.55, origin_y - row * cell_size, 0]))

        for i in range(n - 1):
            for j in range(1, n):
                if j <= i:
                    continue
                display_x = origin_x + (j - 1) * cell_size
                display_y = origin_y - i * cell_size
                value = distortion[i, j] / vmax if vmax else 0.0
                color = interpolate_color(GREEN_D, RED_E, value)
                cell = Rectangle(width=cell_size, height=cell_size, stroke_color=WHITE, fill_color=color, fill_opacity=0.85)
                cell.move_to([display_x, display_y, 0])
                diff = abs(d3[i, j] - d2[i, j])
                main_text = Text(f"{d3[i, j]:.1f}-{d2[i, j]:.1f}", font_size=10, weight="BOLD")
                delta_text = Text(f"~{diff:.1f}", font_size=10)
                cell_text = VGroup(main_text, delta_text).arrange(DOWN, buff=0.03).move_to(cell.get_center())
                grid.add(cell, cell_text)

        legend = VGroup(
            Text("Малое искажение", font_size=16, color=GREEN),
            Text("Большое искажение", font_size=16, color=RED),
        ).arrange(RIGHT, buff=1.4).to_edge(DOWN)

        self.add(title, grid, legend)
