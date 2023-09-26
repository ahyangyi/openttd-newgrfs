import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("industry/industries/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_industry = importlib.import_module(f"industry.industries.{p}")

    __all__.append(p)
    setattr(module, p, _imported_industry.the_industry)
    del _imported_industry
