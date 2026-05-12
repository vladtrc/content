from __future__ import annotations

from _common import documents_figure
from manim import Scene


class InvertedIndexDocuments(Scene):
    def construct(self):
        self.add(documents_figure())
