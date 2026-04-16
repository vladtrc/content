from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourcelessFileLoader
from pathlib import Path


def _load_scene_module():
    anim_dir = Path(__file__).parent
    if str(anim_dir) not in sys.path:
        sys.path.insert(0, str(anim_dir))
    pyc_path = Path(__file__).with_name("__pycache__") / "cube_projection_gif.cpython-314.pyc"
    loader = SourcelessFileLoader("_cube_projection_gif_pyc", str(pyc_path))
    spec = importlib.util.spec_from_loader("_cube_projection_gif_pyc", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


_module = _load_scene_module()


class CubeProjectionAnimation(_module.CubeProjectionAnimation):
    pass
