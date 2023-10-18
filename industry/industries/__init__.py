import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("industry/industries/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    __all__.append(p)
for p in glob.glob("industry/industries/*/__init__.py"):
    p = p.split("/")[-2]
    __all__.append(p)

for p in __all__:
    _imported_industry = importlib.import_module(f"industry.industries.{p}")
    setattr(module, p, _imported_industry.the_industry)
    del _imported_industry
