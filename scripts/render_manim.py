"""Auto-discover and render all manim scenes in animations/ directories.

Convention:
  - *_gif.py       → render as .gif (forward loop)
  - *_loop_gif.py  → render as .gif (forward+reverse ping-pong loop)
  - *.py      → render as .png (static figure)
  - _*.py     → skip (private helpers like _common.py)

Discovery: finds all animations/ dirs next to index.qmd files,
renders each scene into a sibling generated/ directory.
Output filename = snake_case of scene class name.
"""
from __future__ import annotations

import ast
import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_DIR = ROOT / ".manim"


def build_ping_pong_gif(source: Path, output: Path) -> None:
    """Turn a forward gif into a forward+reverse looping gif."""
    command = [
        "magick",
        "(",
        str(source),
        "-coalesce",
        ")",
        "(",
        str(source),
        "-coalesce",
        "-duplicate",
        "-1--2",
        "-reverse",
        ")",
        "-loop",
        "0",
        str(output),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def find_scene_classes(source: Path) -> list[str]:
    """Parse a .py file and return names of classes that inherit from *Scene."""
    tree = ast.parse(source.read_text())
    scenes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                name = base.attr if isinstance(base, ast.Attribute) else getattr(base, "id", "")
                if "Scene" in name:
                    scenes.append(node.name)
                    break
    return scenes


def discover_targets() -> list[dict]:
    """Walk the repo and find all renderable scene files.

    Output filename = py filename without the format suffix.
    e.g. cube_projection_gif.py → cube_projection.gif
         cube_projection_loop_gif.py → cube_projection.gif
         cube_distance_shift.py → cube_distance_shift.png
    One scene class per file expected. If multiple, first is used.
    """
    targets = []
    for anim_dir in sorted(ROOT.rglob("animations")):
        if not anim_dir.is_dir():
            continue
        content_dir = anim_dir.parent
        if not (content_dir / "index.qmd").exists():
            continue

        gen_dir = content_dir / "generated"

        for py_file in sorted(anim_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue

            stem = py_file.stem  # e.g. "cube_projection_gif" or "cube_distance_shift"
            is_ping_pong_gif = stem.endswith("_loop_gif")
            is_gif = stem.endswith("_gif")
            fmt = "gif" if is_gif else "png"
            if is_ping_pong_gif:
                out_name = stem.removesuffix("_loop_gif")
            elif is_gif:
                out_name = stem.removesuffix("_gif")
            else:
                out_name = stem

            scenes = find_scene_classes(py_file)
            if not scenes:
                continue

            targets.append({
                "source": py_file,
                "scene": scenes[0],
                "output": gen_dir / f"{out_name}.{fmt}",
                "format": fmt,
                "ping_pong": is_ping_pong_gif,
                "anim_dir": anim_dir,
            })
    return targets


def normalize_source_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    return path


def select_targets(targets: list[dict], source_path: str | None) -> list[dict]:
    if not source_path:
        return targets

    wanted = normalize_source_path(source_path)
    selected = [target for target in targets if target["source"].resolve() == wanted]
    if not selected:
        raise FileNotFoundError(f"manim scene file not found in discovered targets: {wanted}")
    return selected


def latest_source_mtime(target: dict) -> float:
    return max(py.stat().st_mtime for py in target["anim_dir"].glob("*.py"))


def needs_render(target: dict) -> bool:
    output: Path = target["output"]
    if not output.exists():
        return True
    return latest_source_mtime(target) > output.stat().st_mtime


def bump_qmd_mtime(content_dir: Path) -> None:
    # Touch only the immediate sibling index.qmd. Quarto preview tracks
    # {{< include >}} dependencies, so the aggregate page re-renders on its
    # own. Touching multiple ancestors at once triggered concurrent renders
    # that raced on quarto's sass cache (BadResource: Bad resource ID).
    qmd = content_dir / "index.qmd"
    if qmd.exists():
        now = time.time()
        try:
            os.utime(qmd, (now, now))
        except OSError:
            pass


def render_target(target: dict) -> None:
    output: Path = target["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output_stem = output.stem
    source: Path = target["source"]
    fmt = target["format"]

    if fmt == "gif":
        command = [
            sys.executable, "-m", "manim", "-ql",
            str(source), target["scene"],
            "--media_dir", str(MEDIA_DIR),
            "--format", "gif", "-o", output_stem,
        ]
    else:
        command = [
            sys.executable, "-m", "manim", "-sqh",
            str(source), target["scene"],
            "--media_dir", str(MEDIA_DIR),
            "-o", output_stem,
        ]

    env = os.environ.copy()
    anim_dir = str(target["anim_dir"])
    env["PYTHONPATH"] = anim_dir + (":" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")

    subprocess.run(command, cwd=ROOT, check=True, env=env)

    if fmt == "gif":
        rendered = MEDIA_DIR / "videos" / source.stem / "480p15" / f"{output_stem}.gif"
    else:
        rendered = MEDIA_DIR / "images" / source.stem / f"{output_stem}.png"

    if not rendered.exists():
        raise FileNotFoundError(f"Rendered file not found: {rendered}")

    if fmt == "gif" and target["ping_pong"]:
        build_ping_pong_gif(rendered, output)
    elif fmt == "gif":
        shutil.copy2(rendered, output)
    else:
        shutil.copy2(rendered, output)
    print(f"rendered {output.relative_to(ROOT)}")

    # Nudge quarto preview: touch the sibling index.qmd (and any ancestor
    # index.qmd that might include it) so quarto re-renders and copies the
    # fresh asset into docs/.
    bump_qmd_mtime(target["anim_dir"].parent)


def render_targets(targets: list[dict], changed_only: bool) -> int:
    rendered_any = False
    for target in targets:
        if not target["source"].exists():
            continue
        if changed_only and not needs_render(target):
            continue
        render_target(target)
        rendered_any = True

    if changed_only and not rendered_any:
        print("manim assets are up to date")

    return 0


def stale_targets(targets: list[dict]) -> list[dict]:
    return [target for target in targets if target["source"].exists() and needs_render(target)]


def watch_targets(targets: list[dict], changed_only: bool, interval: float) -> int:
    print(f"watching {len(targets)} manim target(s)")
    render_targets(targets, changed_only=changed_only)
    known_mtimes: dict[Path, float] = {}
    for target in targets:
        if target["source"].exists():
            known_mtimes[target["source"]] = latest_source_mtime(target)

    while True:
        time.sleep(interval)
        targets = discover_targets()
        changed = False
        for target in targets:
            if not target["source"].exists():
                continue
            current = latest_source_mtime(target)
            source = target["source"]
            previous = known_mtimes.get(source)
            if previous is None or current > previous:
                known_mtimes[source] = current
                changed = True

        if not changed:
            continue

        print("detected animation changes, rebuilding")
        render_targets(targets, changed_only=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--watch-interval", type=float, default=1.0)
    parser.add_argument("--source", type=str)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        targets = discover_targets()
        if not targets:
            print("no scenes found")
            return 0

        targets = select_targets(targets, args.source)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        import manim  # noqa: F401
    except ImportError:
        if args.watch or not args.changed_only:
            print("manim is not installed", file=sys.stderr)
            return 1
        missing = stale_targets(targets)
        if not missing:
            print("manim is not installed, but generated assets are up to date")
            return 0
        print("manim is not installed and some generated assets are stale", file=sys.stderr)
        for target in missing:
            print(f"stale: {target['output'].relative_to(ROOT)}", file=sys.stderr)
        return 1

    if args.watch:
        return watch_targets(targets, changed_only=args.changed_only, interval=args.watch_interval)

    return render_targets(targets, changed_only=args.changed_only)


if __name__ == "__main__":
    raise SystemExit(main())
