from __future__ import annotations

from _common import sstable_node
from manim import (
    BLUE_E,
    GREEN_E,
    GREY_B,
    ORANGE,
    UP,
    FadeIn,
    FadeOut,
    ReplacementTransform,
    Scene,
    Text,
    VGroup,
)


class LsmPipelineGif(Scene):
    memtable_capacity = 4
    memtable_y = 2.3
    l0_y = 0.3
    l1_y = -1.9
    incoming_y = 3.3
    l0_spacing = 3.4

    def construct(self):
        self._setup_labels()

        self.memtable = self._memtable([])
        self.add(self.memtable)

        self.l0_sstables: list[VGroup] = []
        self.l0_keys: list[list[int]] = []

        self._run_batch([5, 2, 8])
        self._run_batch([7, 3, 1])

        self.wait(0.3)
        self._compaction()
        self.wait(1.6)

    def _setup_labels(self) -> None:
        for y, text in [
            (self.memtable_y, "Memtable"),
            (self.l0_y, "L0"),
            (self.l1_y, "L1"),
        ]:
            self.add(
                Text(text, font_size=20, weight="BOLD", color=GREY_B).move_to(
                    [-5.6, y, 0]
                )
            )

    def _memtable(self, keys: list[int]) -> VGroup:
        node = sstable_node(
            [str(k) for k in keys],
            color=GREEN_E,
            capacity=self.memtable_capacity,
        )
        node.move_to([0, self.memtable_y, 0])
        return node

    def _run_batch(self, values: list[int]) -> None:
        sorted_keys: list[int] = []
        for value in values:
            incoming = Text(
                str(value), font_size=30, weight="BOLD"
            ).move_to([0, self.incoming_y, 0])
            self.play(FadeIn(incoming, shift=UP * 0.3), run_time=0.4)
            sorted_keys = sorted(sorted_keys + [value])
            new_memtable = self._memtable(sorted_keys)
            self.play(
                ReplacementTransform(self.memtable, new_memtable),
                FadeOut(incoming),
                run_time=0.55,
            )
            self.memtable = new_memtable
            self.wait(0.1)

        slot = len(self.l0_sstables)
        l0_x = -2.2 + slot * self.l0_spacing
        flushed = sstable_node(
            [str(k) for k in sorted_keys], color=BLUE_E, capacity=4
        ).move_to([l0_x, self.l0_y, 0])

        flush_caption = Text(
            "flush", font_size=18, color=BLUE_E
        ).move_to([l0_x, (self.memtable_y + self.l0_y) / 2, 0])
        self.play(FadeIn(flush_caption), run_time=0.25)
        self.play(ReplacementTransform(self.memtable, flushed), run_time=0.9)
        self.play(FadeOut(flush_caption), run_time=0.2)

        self.l0_sstables.append(flushed)
        self.l0_keys.append(sorted_keys)

        self.memtable = self._memtable([])
        self.play(FadeIn(self.memtable), run_time=0.25)

    def _compaction(self) -> None:
        merged_keys = sorted(k for keys in self.l0_keys for k in keys)
        merged = sstable_node(
            [str(k) for k in merged_keys],
            color=ORANGE,
            capacity=len(merged_keys),
            font_size=22,
        ).move_to([0, self.l1_y, 0])

        caption = Text(
            "compaction", font_size=18, color=ORANGE
        ).move_to([0, (self.l0_y + self.l1_y) / 2, 0])
        self.play(FadeIn(caption), run_time=0.3)
        self.play(
            *[
                ReplacementTransform(sst, merged.copy())
                for sst in self.l0_sstables
            ],
            run_time=1.2,
        )
        self.add(merged)
        self.play(FadeOut(caption), run_time=0.25)
