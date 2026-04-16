from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, WHITE,
    Arrow, BLUE_D, BLUE_E, GREEN_E, Line,
    Rectangle, RoundedRectangle, Scene, Text, VGroup,
)


class BTreeNodeDiagram(VGroup):
    def __init__(self, keys: list[str], labels: list[str] | None = None, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.1, color=BLUE_E)
        separators = VGroup(
            Line(box.get_top() + LEFT * 1.15, box.get_bottom() + LEFT * 1.15, color=BLUE_D),
            Line(box.get_top(), box.get_bottom(), color=BLUE_D),
            Line(box.get_top() + RIGHT * 1.15, box.get_bottom() + RIGHT * 1.15, color=BLUE_D),
        )
        key_text = VGroup(
            *[
                Text(text, font_size=28, weight="BOLD").move_to(box.get_center() + shift)
                for text, shift in zip(keys, [LEFT * 1.7, LEFT * 0.55, RIGHT * 0.6], strict=True)
            ]
        )
        self.add(box, separators, key_text)

        if labels:
            arrows = VGroup()
            children = VGroup()
            boundary_x = [
                box.get_left()[0],
                box.get_left()[0] + box.width / 4,
                box.get_left()[0] + box.width / 2,
                box.get_left()[0] + 3 * box.width / 4,
            ]
            anchors = [
                [x, box.get_bottom()[1], 0]
                for x in boundary_x
            ]
            x_offsets = [-2.2, -0.9, 0.75, 2.1]
            for anchor, label, x_offset in zip(anchors, labels, x_offsets, strict=True):
                child = Text(label, font_size=18).move_to(box.get_bottom() + DOWN * 1.3 + RIGHT * x_offset)
                arrow = Arrow(anchor, child.get_top() + UP * 0.05, buff=0.06, stroke_width=2.4, max_tip_length_to_length_ratio=0.12)
                arrows.add(arrow)
                children.add(child)
            self.add(arrows, children)


def simple_node(keys: list[str], color=BLUE_E, capacity: int | None = None) -> VGroup:
    cell_width = 0.8
    capacity = max(len(keys), capacity or len(keys), 1)
    width = max(1.0, capacity * cell_width)
    rect = RoundedRectangle(corner_radius=0.1, width=width, height=0.65, color=color)
    group = VGroup(rect)
    if capacity > 1:
        for index in range(1, capacity):
            x = rect.get_left()[0] + cell_width * index
            group.add(Line([x, rect.get_top()[1], 0], [x, rect.get_bottom()[1], 0], color=color))
    for index, key in enumerate(keys):
        center_x = rect.get_left()[0] + cell_width * (index + 0.5)
        group.add(Text(key, font_size=24, weight="BOLD").move_to([center_x, rect.get_center()[1], 0]))
    return group


def stage_group(label: str, root_keys: list[str], left_keys: list[str] | None = None, right_keys: list[str] | None = None) -> VGroup:
    caption = Text(label, font_size=24, weight="BOLD")
    root = simple_node(root_keys, color=GREEN_E if left_keys else BLUE_E)
    graph = VGroup(root)
    if left_keys and right_keys:
        left = simple_node(left_keys, color=BLUE_D)
        right = simple_node(right_keys, color=BLUE_D)
        left.next_to(root, DOWN, buff=1.0).shift(LEFT * 0.9)
        right.next_to(root, DOWN, buff=1.0).shift(RIGHT * 0.9)
        graph.add(
            left, right,
            Line(root.get_bottom() + LEFT * 0.25, left.get_top(), color=WHITE),
            Line(root.get_bottom() + RIGHT * 0.25, right.get_top(), color=WHITE),
        )
    graph.next_to(caption, DOWN, buff=0.35)
    return VGroup(caption, graph)
