from __future__ import annotations

import math

import numpy as np
from manim import Axes, Dot, GREY_B, Line, RED_E, Text, VGroup, WHITE, DOWN, LEFT


def random_projection(points: np.ndarray, target_dim: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(points.shape[1], target_dim)) / math.sqrt(target_dim)
    return points @ matrix


def orthographic_projection_xy(points: np.ndarray) -> np.ndarray:
    return points[:, :2]


def rotate_x(points: np.ndarray, degrees: float) -> np.ndarray:
    radians = np.deg2rad(degrees)
    c, s = np.cos(radians), np.sin(radians)
    return points @ np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float).T


def rotate_y(points: np.ndarray, degrees: float) -> np.ndarray:
    radians = np.deg2rad(degrees)
    c, s = np.cos(radians), np.sin(radians)
    return points @ np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float).T


def rotate_z(points: np.ndarray, degrees: float) -> np.ndarray:
    radians = np.deg2rad(degrees)
    c, s = np.cos(radians), np.sin(radians)
    return points @ np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float).T


def nice_cube_orientation(points: np.ndarray) -> np.ndarray:
    return rotate_z(rotate_y(rotate_x(points, 28), -22), 18)


def cube_vertices() -> np.ndarray:
    return np.array([
        [-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
        [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1],
    ], dtype=float)


def cube_edges() -> list[tuple[int, int]]:
    verts = cube_vertices()
    return [(i, j) for i in range(8) for j in range(i + 1, 8)
            if np.sum(np.abs(verts[i] - verts[j])) == 2]


def point_labels() -> list[str]:
    return list("ABCDEFGH")


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    diffs = points[:, None, :] - points[None, :, :]
    distances = np.linalg.norm(diffs, axis=-1)
    return distances[np.triu_indices(len(points), k=1)]


def relative_distortion(original: np.ndarray, projected: np.ndarray) -> np.ndarray:
    baseline = np.where(original == 0, 1e-12, original)
    return np.abs(projected - original) / baseline


def mean_relative_distortion(original: np.ndarray, projected: np.ndarray) -> float:
    return float(np.mean(relative_distortion(original, projected)))


def scaled_random_points(
    rng: np.random.Generator, source_dim: int, n_points: int, target_median_distance: float,
) -> np.ndarray:
    points = rng.normal(size=(n_points, source_dim))
    current_median = float(np.median(pairwise_distances(points)))
    scale = target_median_distance / current_median if current_median > 0 else 1.0
    return points * scale


def make_scatter_axes(x_values: np.ndarray, y_values: np.ndarray, title: str, subtitle: str, width: float = 4.8, height: float = 3.8) -> VGroup:
    lo = float(min(x_values.min(), y_values.min()))
    hi = float(max(x_values.max(), y_values.max()))
    padding = (hi - lo) * 0.08 if hi > lo else 0.2
    x_range = [lo - padding, hi + padding, max((hi - lo) / 4, 0.5)]
    axes = Axes(
        x_range=x_range, y_range=x_range,
        x_length=width, y_length=height,
        axis_config={"color": GREY_B, "include_numbers": False, "stroke_width": 2},
        tips=False,
    )
    diagonal = Line(axes.c2p(lo - padding, lo - padding), axes.c2p(hi + padding, hi + padding), color=WHITE, stroke_width=2)
    dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.05, color=RED_E) for x, y in zip(x_values, y_values, strict=True)])
    header = VGroup(
        Text(title, font_size=24, weight="BOLD"),
        Text(subtitle, font_size=18, color=GREY_B),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    chart = VGroup(axes, diagonal, dots)
    chart.next_to(header, DOWN, buff=0.22)
    return VGroup(header, chart)
