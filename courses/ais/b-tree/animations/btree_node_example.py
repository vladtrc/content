from __future__ import annotations

from _common import BTreeNodeDiagram
from manim import UP, Scene


class BTreeNodeExample(Scene):
    def construct(self):
        diagram = BTreeNodeDiagram(
            keys=["15", "30", "50"],
            labels=["p0: < 15", "p1: [15, 30)", "p2: [30, 50)", "p3: >= 50"],
        ).move_to(UP * 0.6)
        self.add(diagram)
