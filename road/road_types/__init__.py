import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("road/road_types/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_road_type = importlib.import_module(f"road.road_types.{p}")

    __all__.append(p)
    setattr(module, p, _imported_road_type.the_road_type)
    del _imported_road_type
