from __future__ import annotations

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
    Circle,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
)

FONT = "FreeSans"


def node(label: str, *, terminal: bool = False, radius: float = 0.3) -> VGroup:
    color = ORANGE if terminal else BLUE_E
    circ = Circle(radius=radius, color=color, stroke_width=2)
    txt = Text(label, font=FONT, font_size=18, color=WHITE)
    txt.move_to(circ)
    return VGroup(circ, txt)


def chain_node(label: str, *, terminal: bool = False) -> VGroup:
    color = ORANGE if terminal else BLUE_E
    rect = RoundedRectangle(
        corner_radius=0.1,
        width=max(0.8, 0.3 + 0.22 * len(label)),
        height=0.5,
        color=color,
        stroke_width=2,
    )
    txt = Text(label, font=FONT, font_size=18, color=WHITE)
    txt.move_to(rect)
    return VGroup(rect, txt)


def edge(a: VGroup, b: VGroup, *, label: str | None = None) -> VGroup:
    line = Line(a.get_bottom(), b.get_top(), color=GREY_B, stroke_width=1.6)
    g = VGroup(line)
    if label:
        lbl = Text(label, font=FONT, font_size=14, color=GREY_B)
        lbl.move_to((a.get_bottom() + b.get_top()) / 2 + RIGHT * 0.1)
        g.add(lbl)
    return g


class TrieRadix(Scene):
    def construct(self):
        title = Text(
            "Trie vs Radix trie  —  car, cat, cart, dog",
            font=FONT,
            font_size=28,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.4)

        # Left: classic trie
        left_caption = Text("Trie (по 1 символу на ребро)", font=FONT, font_size=20)
        left_caption.move_to(LEFT * 3.6 + UP * 2.4)

        root1 = node("·")
        root1.move_to(LEFT * 3.6 + UP * 1.7)

        c = node("c")
        d = node("d")
        c.move_to(LEFT * 4.4 + UP * 0.8)
        d.move_to(LEFT * 2.6 + UP * 0.8)

        a1 = node("a")
        a1.move_to(LEFT * 4.4 + DOWN * 0.0)

        r1 = node("r", terminal=True)  # 'car'
        t1 = node("t", terminal=True)  # 'cat'
        r1.move_to(LEFT * 5.0 + DOWN * 0.9)
        t1.move_to(LEFT * 3.8 + DOWN * 0.9)

        t2 = node("t", terminal=True)  # 'cart'
        t2.move_to(LEFT * 5.0 + DOWN * 1.85)

        o = node("o")
        g = node("g", terminal=True)  # 'dog'
        o.move_to(LEFT * 2.6 + DOWN * 0.0)
        g.move_to(LEFT * 2.6 + DOWN * 0.9)

        left = VGroup(
            left_caption, root1, c, d, a1, r1, t1, t2, o, g,
            edge(root1, c), edge(root1, d),
            edge(c, a1), edge(d, o),
            edge(a1, r1), edge(a1, t1),
            edge(r1, t2),
            edge(o, g),
        )

        # Right: radix
        right_caption = Text("Radix trie (склейка цепочек)", font=FONT, font_size=20)
        right_caption.move_to(RIGHT * 3.6 + UP * 2.4)

        root2 = node("·")
        root2.move_to(RIGHT * 3.6 + UP * 1.7)

        ca = chain_node("ca")
        dog = chain_node("dog", terminal=True)
        ca.move_to(RIGHT * 2.8 + UP * 0.5)
        dog.move_to(RIGHT * 4.6 + UP * 0.5)

        r2 = chain_node("r", terminal=True)
        t3 = chain_node("t", terminal=True)
        r2.move_to(RIGHT * 2.0 + DOWN * 0.6)
        t3.move_to(RIGHT * 3.6 + DOWN * 0.6)

        t4 = chain_node("t", terminal=True)
        t4.move_to(RIGHT * 2.0 + DOWN * 1.7)

        right = VGroup(
            right_caption, root2, ca, dog, r2, t3, t4,
            edge(root2, ca), edge(root2, dog),
            edge(ca, r2), edge(ca, t3),
            edge(r2, t4),
        )

        legend = Text(
            "оранжевый = конец слова   ·  radix сливает цепочки одного ребёнка → меньше узлов в памяти",
            font=FONT,
            font_size=15,
            color=GREY_B,
        )
        legend.to_edge(DOWN, buff=0.4)

        self.add(title, left, right, legend)
