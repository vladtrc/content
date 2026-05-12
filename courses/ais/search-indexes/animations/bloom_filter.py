from __future__ import annotations

from manim import (
    BLUE_E,
    DOWN,
    GREEN_E,
    GREY_B,
    GREY_E,
    LEFT,
    ORANGE,
    RED_E,
    RIGHT,
    UP,
    WHITE,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def bit_array(bits: list[int], highlight: dict[int, str] | None = None) -> VGroup:
    highlight = highlight or {}
    cell_w = 0.45
    cells = VGroup()
    for i, b in enumerate(bits):
        col = BLUE_E
        if i in highlight:
            col = {"set": GREEN_E, "probe_hit": ORANGE, "probe_miss": RED_E}[highlight[i]]
        rect = Rectangle(
            width=cell_w,
            height=cell_w,
            color=col,
            fill_color=col if b else GREY_E,
            fill_opacity=0.9 if b else 0.2,
            stroke_width=1.5,
        )
        txt = Text(str(b), font=FONT, font_size=16, color=WHITE if b else GREY_B)
        txt.move_to(rect)
        cells.add(VGroup(rect, txt))
    cells.arrange(RIGHT, buff=0.04)
    return cells


class BloomFilter(Scene):
    def construct(self):
        title = Text(
            "Bloom filter: «точно нет» за пару хешей",
            font=FONT,
            font_size=28,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        # Bit array of size 16
        bits = [0] * 16
        # Insert "alice" -> hashes 2, 7, 13
        for h in (2, 7, 13):
            bits[h] = 1
        # Insert "bob" -> hashes 1, 7, 11
        for h in (1, 7, 11):
            bits[h] = 1

        # Probe "carol" -> hashes 4, 9, 11 -> bit 4 = 0 -> definitely not in set
        # Probe "alice" -> all three bits set -> probably yes
        array = bit_array(bits)

        array_label = Text("bits[0..15]", font=FONT, font_size=18, color=GREY_B)
        array_label.next_to(array, LEFT, buff=0.3)

        array_group = VGroup(array_label, array)
        array_group.move_to(UP * 0.4)

        # Inserted items
        ins_text = Text(
            'insert: «alice» → h1=2, h2=7, h3=13;   «bob» → h1=1, h2=7, h3=11',
            font=FONT,
            font_size=18,
            color=GREEN_E,
        )
        ins_text.next_to(array_group, DOWN, buff=0.5)

        # Probes
        probe1 = Text(
            'lookup «carol» → h=4: bit=0  → точно НЕТ (false negative невозможен)',
            font=FONT,
            font_size=18,
            color=RED_E,
        )
        probe2 = Text(
            'lookup «alice» → h={2,7,13}: все bit=1 → «вероятно есть» (нужно подтвердить)',
            font=FONT,
            font_size=18,
            color=ORANGE,
        )
        probes = VGroup(probe1, probe2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        probes.next_to(ins_text, DOWN, buff=0.45)

        note = Text(
            "False positive возможен, false negative — нет. Выигрываем I/O перед чтением SSTable.",
            font=FONT,
            font_size=17,
            color=GREY_B,
        )
        note.to_edge(DOWN, buff=0.4)

        self.add(title, array_group, ins_text, probes, note)
