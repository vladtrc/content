from __future__ import annotations

from _common import sstable_node
from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    LEFT,
    ORANGE,
    RIGHT,
    UP,
    WHITE,
    Arrow,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)


class LsmStructure(Scene):
    def construct(self):
        # Memory layer: WAL + Memtable
        wal = self._box("WAL", "append-only журнал", color=GREY_B)
        memtable = self._box("Memtable", "skip-list в памяти", color=GREEN_E)
        memory_row = VGroup(wal, memtable).arrange(RIGHT, buff=0.6)
        memory_row.move_to(UP * 2.5)
        memory_label = Text("Память", font_size=18, color=GREY_B).next_to(
            memory_row, UP, buff=0.15
        )

        # L0 layer: multiple SSTables
        l0_sstables = VGroup(
            *[
                self._sstable_with_bloom(keys)
                for keys in [["2", "5", "8"], ["1", "3", "7"], ["4", "6", "9"]]
            ]
        ).arrange(RIGHT, buff=0.5)
        l0_sstables.move_to(UP * 0.0)
        l0_label = Text("L0", font_size=18, color=GREY_B).next_to(
            l0_sstables, LEFT, buff=0.4
        )

        # L1 layer: merged SSTable
        l1_sstable = self._sstable_with_bloom(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        )
        l1_sstable.move_to(DOWN * 2.2)
        l1_label = Text("L1", font_size=18, color=GREY_B).next_to(
            l1_sstable, LEFT, buff=0.4
        )

        # Arrows
        flush_arrow = Arrow(
            memory_row.get_bottom() + DOWN * 0.05,
            l0_sstables.get_top() + UP * 0.05,
            buff=0.1,
            stroke_width=3,
            color=BLUE_E,
        )
        flush_label = Text("flush", font_size=16, color=BLUE_E).next_to(
            flush_arrow, RIGHT, buff=0.15
        )

        compaction_arrow = Arrow(
            l0_sstables.get_bottom() + DOWN * 0.05,
            l1_sstable.get_top() + UP * 0.05,
            buff=0.1,
            stroke_width=3,
            color=ORANGE,
        )
        compaction_label = Text(
            "compaction", font_size=16, color=ORANGE
        ).next_to(compaction_arrow, RIGHT, buff=0.15)

        self.add(
            memory_label,
            memory_row,
            l0_label,
            l0_sstables,
            l1_label,
            l1_sstable,
            flush_arrow,
            flush_label,
            compaction_arrow,
            compaction_label,
        )

    def _box(self, title: str, subtitle: str, color) -> VGroup:
        rect = RoundedRectangle(
            corner_radius=0.12, width=2.8, height=1.0, color=color
        )
        title_text = Text(title, font_size=22, weight="BOLD").move_to(
            rect.get_center() + UP * 0.18
        )
        subtitle_text = Text(subtitle, font_size=14, color=GREY_B).move_to(
            rect.get_center() + DOWN * 0.22
        )
        return VGroup(rect, title_text, subtitle_text)

    def _sstable_with_bloom(self, keys: list[str]) -> VGroup:
        node = sstable_node(keys, color=BLUE_E)
        bloom = Text("Bloom", font_size=12, color=GREY_B).next_to(
            node, DOWN, buff=0.1
        )
        return VGroup(node, bloom)
