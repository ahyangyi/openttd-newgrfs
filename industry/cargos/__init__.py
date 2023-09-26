import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("industry/cargos/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_cargo = importlib.import_module(f"industry.cargos.{p}")

    __all__.append(p)
    setattr(module, p, _imported_cargo.the_cargo)
    del _imported_cargo
