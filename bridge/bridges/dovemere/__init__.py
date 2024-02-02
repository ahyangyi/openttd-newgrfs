import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("bridge/bridges/dovemere/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    _imported_bridge_type = importlib.import_module(f"bridge.bridges.dovemere.{p}")

    __all__.append(p)
    setattr(module, p, _imported_bridge_type.the_bridge)
    del _imported_bridge_type
