from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, WHITE, Line, Scene, VGroup

from _common import simple_node


class BTreeInsertProgression(Scene):
    def construct(self):
        stage_1 = VGroup(simple_node(["1", "2"]))
        stage_2 = VGroup(simple_node(["1", "2", "3"]))
        stage_3 = self.split_state(["1"], ["3", "4"])
        stage_4 = self.split_state(["1"], ["3", "4", "5"])

        row = VGroup(stage_1, stage_2, stage_3, stage_4).arrange(RIGHT, buff=0.7).scale(0.82)
        row.move_to(DOWN * 0.1)

        self.add(row)

    def split_state(self, left_keys: list[str], right_keys: list[str]) -> VGroup:
        root = simple_node(["2"])
        left = simple_node(left_keys)
        right = simple_node(right_keys)
        left.move_to(root.get_center() + DOWN * 1.35 + LEFT * 1.1)
        right.move_to(root.get_center() + DOWN * 1.35 + RIGHT * 1.1)
        links = VGroup(
            Line(root.get_bottom() + DOWN * 0.02, left.get_top(), color=WHITE),
            Line(root.get_bottom() + DOWN * 0.02, right.get_top(), color=WHITE),
        )
        return VGroup(root, left, right, links)
