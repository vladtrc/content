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
    TEAL_E,
    UP,
    WHITE,
    Line,
    RoundedRectangle,
    Text,
    VGroup,
)


FONT = "FreeSans"
TERM_COLORS = {
    "cat": ORANGE,
    "sat": TEAL_E,
    "dog": RED_E,
    "ran": GREEN_E,
}


def documents_figure() -> VGroup:
    title = Text("Исходные документы", font=FONT, font_size=34, weight="BOLD")
    title.to_edge(UP, buff=0.45)

    docs = VGroup(
        document_card("Doc1", ["cat", "sat"]),
        document_card("Doc2", ["sat", "dog"]),
        document_card("Doc3", ["cat", "ran"]),
        document_card("Doc4", ["cat", "sat", "sat"], highlight=True),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    docs.move_to(DOWN * 0.15)

    note = Text(
        "Каждый документ сначала разбивается на токены",
        font=FONT,
        font_size=19,
        color=GREY_B,
    )
    note.next_to(docs, DOWN, buff=0.28)

    return VGroup(title, docs, note)


def document_card(
    doc_id: str,
    terms: list[str],
    *,
    width: float = 4.2,
    highlight: bool = False,
    deleted: bool = False,
) -> VGroup:
    border_color = BLUE_E if highlight else GREY_B
    rect = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=0.72,
        color=border_color,
        stroke_width=2.6 if highlight else 1.7,
    )

    label = Text(doc_id, font=FONT, font_size=20, weight="BOLD", color=WHITE)
    label.move_to(rect.get_left() + RIGHT * 0.62)

    tokens = VGroup(
        *[
            Text(term, font=FONT, font_size=22, color=TERM_COLORS[term])
            for term in terms
        ]
    ).arrange(RIGHT, buff=0.18)
    tokens.move_to(rect.get_center() + RIGHT * 0.7)

    group = VGroup(rect, label, tokens)
    if deleted:
        strike = Line(
            rect.get_left() + RIGHT * 0.2,
            rect.get_right() + LEFT * 0.2,
            color=RED_E,
            stroke_width=4,
        )
        tombstone = Text("deleted", font=FONT, font_size=15, color=RED_E)
        tombstone.next_to(rect, RIGHT, buff=0.12)
        group.add(strike, tombstone)
    return group


def posting_row(
    term: str,
    postings: list[str],
    *,
    deleted_values: set[str] | None = None,
) -> VGroup:
    deleted_values = deleted_values or set()
    term_text = Text(
        term, font=FONT, font_size=24, weight="BOLD", color=TERM_COLORS[term]
    )
    arrow = Text("->", font=FONT, font_size=22, color=GREY_B)
    cells = VGroup(
        *[
            posting_cell(value, deleted=value in deleted_values)
            for value in postings
        ]
    ).arrange(RIGHT, buff=0.12)
    return VGroup(term_text, arrow, cells).arrange(RIGHT, buff=0.18)


def posting_cell(value: str, *, deleted: bool = False, accent: bool = False) -> VGroup:
    width = max(0.72, 0.2 * len(value) + 0.34)
    color = RED_E if deleted else BLUE_E if accent else GREY_B
    rect = RoundedRectangle(
        corner_radius=0.09,
        width=width,
        height=0.46,
        color=color,
        fill_color=GREY_E,
        fill_opacity=0.52,
        stroke_width=2.0 if accent or deleted else 1.5,
    )
    text = Text(value, font=FONT, font_size=15, color=RED_E if deleted else WHITE)
    text.move_to(rect)
    group = VGroup(rect, text)
    if deleted:
        group.add(Line(rect.get_left(), rect.get_right(), color=RED_E, stroke_width=2.8))
    return group
