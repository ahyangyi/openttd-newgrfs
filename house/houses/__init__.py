import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("house/houses/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    __all__.append(p)

for p in __all__:
    _imported_house = importlib.import_module(f"house.houses.{p}")
    setattr(module, p, _imported_house.the_house)
    del _imported_house
