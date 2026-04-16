from __future__ import annotations

from manim import (
    BLUE_E,
    BLUE_D,
    GREEN_E,
    GREY_B,
    LEFT,
    RIGHT,
    RoundedRectangle,
    Line,
    Text,
    VGroup,
)


CELL_WIDTH = 0.8
CELL_HEIGHT = 0.65


def sstable_node(
    keys: list[str],
    color=BLUE_E,
    capacity: int | None = None,
    font_size: int = 24,
) -> VGroup:
    capacity = max(len(keys), capacity or len(keys), 1)
    width = max(1.0, capacity * CELL_WIDTH)
    rect = RoundedRectangle(
        corner_radius=0.1, width=width, height=CELL_HEIGHT, color=color
    )
    group = VGroup(rect)
    for index in range(1, capacity):
        x = rect.get_left()[0] + CELL_WIDTH * index
        group.add(
            Line(
                [x, rect.get_top()[1], 0],
                [x, rect.get_bottom()[1], 0],
                color=color,
            )
        )
    for index, key in enumerate(keys):
        center_x = rect.get_left()[0] + CELL_WIDTH * (index + 0.5)
        group.add(
            Text(key, font_size=font_size, weight="BOLD").move_to(
                [center_x, rect.get_center()[1], 0]
            )
        )
    return group


def labeled_layer(label: str, font_size: int = 22) -> Text:
    return Text(label, font_size=font_size, weight="BOLD", color=GREY_B)
