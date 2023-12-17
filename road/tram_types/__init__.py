import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("road/tram_types/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_tram_type = importlib.import_module(f"road.tram_types.{p}")

    __all__.append(p)
    setattr(module, p, _imported_tram_type.the_tram_type)
    del _imported_tram_type
