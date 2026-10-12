"""Game projects built with this engine, wherever they are: engine.blk (how the project and its programs find the
engine), the project's CMakePresets.json (presets), and creating and relinking them (create: dng.py new and relink in
the engine root)."""
from .engine import ENGINE_BLK, ProjectError, read_engine_root, write_engine_blk
