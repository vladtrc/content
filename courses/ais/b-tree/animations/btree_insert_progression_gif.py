from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass, field

from _common import simple_node
from manim import (
    BLUE_E,
    DOWN,
    RED_E,
    RIGHT,
    UP,
    WHITE,
    FadeIn,
    Line,
    Scene,
    Text,
    TransformMatchingShapes,
    VGroup,
)


@dataclass
class BTreeNode:
    keys: list[int]
    children: list["BTreeNode"] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return not self.children


class BTreeTracer:
    def __init__(self, max_keys: int = 3):
        self.max_keys = max_keys
        self.root: BTreeNode | None = None
        self.split_detected = False

    def build_steps(self, values: list[int]) -> list[dict]:
        steps = []
        for value in values:
            target_path = self.find_leaf_path(value)
            split_happened = self.insert(value)
            after = self.to_spec()
            step = {"insert": str(value), "after": after}
            if split_happened:
                step["highlight"] = self.highlight_for_path(target_path)
                step["restructured"] = self.spec_without_key(after, value)
            steps.append(step)
        return steps

    def insert(self, value: int) -> bool:
        self.split_detected = False
        if self.root is None:
            self.root = BTreeNode([value])
            return False

        split_result = self.insert_into_node(self.root, value)
        if split_result is not None:
            promoted, right = split_result
            left = self.root
            self.root = BTreeNode([promoted], [left, right])
            self.split_detected = True

        return self.split_detected

    def insert_into_node(self, node: BTreeNode, value: int) -> tuple[int, BTreeNode] | None:
        if node.is_leaf:
            node.keys.append(value)
            node.keys.sort()
        else:
            child_index = bisect_right(node.keys, value)
            split_result = self.insert_into_node(node.children[child_index], value)
            if split_result is not None:
                promoted, right = split_result
                node.keys.insert(child_index, promoted)
                node.children.insert(child_index + 1, right)

        if len(node.keys) <= self.max_keys:
            return None

        self.split_detected = True
        return self.split_node(node)

    def split_node(self, node: BTreeNode) -> tuple[int, BTreeNode]:
        promoted_index = len(node.keys) // 2
        promoted = node.keys[promoted_index]
        right_keys = node.keys[promoted_index + 1 :]
        node.keys = node.keys[:promoted_index]

        if node.is_leaf:
            right_children: list[BTreeNode] = []
        else:
            right_children = node.children[promoted_index + 1 :]
            node.children = node.children[: promoted_index + 1]

        return promoted, BTreeNode(right_keys, right_children)

    def find_leaf_path(self, value: int) -> list[int]:
        if self.root is None:
            return []

        path = []
        node = self.root
        while not node.is_leaf:
            child_index = bisect_right(node.keys, value)
            path.append(child_index)
            node = node.children[child_index]
        return path

    def highlight_for_path(self, path: list[int]) -> dict:
        if not path:
            return {"root": True}
        return {"children": [path[0]]}

    def to_spec(self) -> dict:
        if self.root is None:
            raise ValueError("tree is empty")

        spec = {"root": [str(key) for key in self.root.keys]}
        if self.root.children:
            spec["children"] = [
                {"slot": slot, "keys": [str(key) for key in child.keys]}
                for slot, child in enumerate(self.root.children)
            ]
        return spec

    def spec_without_key(self, spec: dict, value: int) -> dict:
        value_text = str(value)
        trimmed = {
            "root": list(spec["root"]),
            "children": [
                {"slot": child["slot"], "keys": list(child["keys"])}
                for child in spec.get("children", [])
            ],
        }

        for child in trimmed["children"]:
            if value_text in child["keys"]:
                child["keys"].remove(value_text)
                return trimmed

        if value_text in trimmed["root"]:
            trimmed["root"].remove(value_text)
        return trimmed


class BTreeInsertProgressionGif(Scene):
    cell_width = 0.8
    incoming_center = UP * 3.1
    root_center = UP * 1.65
    child_center = DOWN * 0.95
    child_gap = 2.0
    node_scale = 1.25

    def construct(self):
        steps = BTreeTracer(max_keys=3).build_steps([8, 21, 34, 55, 63, 77, 84, 96])

        current = None
        for spec in steps:
            incoming = self.make_incoming_key(spec["insert"])
            self.play(FadeIn(incoming, shift=UP * 0.35), run_time=0.45)
            self.wait(0.15)

            if current is not None and spec.get("highlight"):
                highlighted = self.tree_state(
                    current["spec"], highlight=spec["highlight"]
                )
                self.play(
                    TransformMatchingShapes(current["state"], highlighted),
                    run_time=0.55,
                )
                current = {"spec": current["spec"], "state": highlighted}
                self.wait(0.2)

                restructured = self.tree_state(spec["restructured"])
                self.play(
                    TransformMatchingShapes(current["state"], restructured),
                    run_time=2.7,
                )
                current = {"spec": spec["restructured"], "state": restructured}
                self.wait(0.25)

            next_state = self.tree_state(spec["after"])
            source = (
                VGroup(incoming)
                if current is None
                else VGroup(current["state"], incoming)
            )
            self.play(TransformMatchingShapes(source, next_state), run_time=1.0)
            current = {"spec": spec["after"], "state": next_state}
            self.wait(0.35)

        self.wait(1.4)

    def tree_state(self, spec: dict, highlight: dict | None = None) -> VGroup:
        highlight = highlight or {}
        root_color = RED_E if highlight.get("root") else BLUE_E
        root = self.make_node(spec["root"], self.root_center, color=root_color)
        state = VGroup(root)

        children_spec = spec.get("children")
        if not children_spec:
            return state

        ordered_children = self.normalize_children(spec["root"], children_spec)
        children = self.build_children(
            ordered_children, set(highlight.get("children", []))
        )
        links = self.build_links(root, spec["root"], children, ordered_children)
        state.add(children, links)
        return state

    def make_node(self, keys: list[str], center, color=BLUE_E) -> VGroup:
        capacity = max(3 if len(keys) <= 3 else len(keys), 1)
        node = simple_node(keys, color=color, capacity=capacity)
        node.scale(self.node_scale)
        node.move_to(center)
        return node

    def make_incoming_key(self, key: str) -> VGroup:
        return VGroup(
            Text(key, font_size=30, weight="BOLD", color=WHITE).move_to(
                self.incoming_center
            )
        )

    def normalize_children(
        self, root_keys: list[str], child_specs: list[dict]
    ) -> list[dict]:
        ordered = sorted(child_specs, key=lambda child: child["slot"])
        actual_slots = [child["slot"] for child in ordered]
        expected_slots = list(range(len(root_keys) + 1))
        if actual_slots != expected_slots:
            raise ValueError(
                f"expected child slots {expected_slots}, got {actual_slots}"
            )
        return ordered

    def build_children(
        self, child_specs: list[dict], highlighted_slots: set[int]
    ) -> VGroup:
        children = VGroup(
            *[
                self.make_node(
                    child["keys"],
                    self.child_center,
                    color=RED_E if child["slot"] in highlighted_slots else BLUE_E,
                )
                for child in child_specs
            ]
        )
        children.arrange(RIGHT, buff=self.child_gap)
        children.move_to(self.child_center)
        return children

    def build_links(
        self,
        root: VGroup,
        root_keys: list[str],
        children: VGroup,
        child_specs: list[dict],
    ) -> VGroup:
        links = VGroup()
        slot_positions = self.link_positions(root, len(root_keys))
        for child, child_spec in zip(children, child_specs, strict=True):
            slot_x = slot_positions[child_spec["slot"]]
            links.add(
                Line(
                    [slot_x, root.get_bottom()[1] - 0.03, 0],
                    child.get_top() + UP * 0.03,
                    color=WHITE,
                )
            )
        return links

    def link_positions(self, root: VGroup, key_count: int) -> list[float]:
        rect = root[0]
        left_x = rect.get_left()[0]
        scaled_cell_width = self.cell_width * self.node_scale
        return [left_x + scaled_cell_width * slot for slot in range(key_count + 1)]
