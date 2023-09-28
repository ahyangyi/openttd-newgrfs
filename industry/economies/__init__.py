import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("industry/economies/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_economy = importlib.import_module(f"industry.economies.{p}")

    __all__.append(p)
    setattr(module, p, _imported_economy.TheEconomy())
    del _imported_economy
