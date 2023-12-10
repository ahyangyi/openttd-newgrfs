import sys
import glob
import importlib

module = sys.modules[__name__]

__all__ = []
for p in glob.glob("road_vehicle/vehicles/lorries/*.py"):
    p = p.split("/")[-1][:-3]
    if p == "__init__":
        continue
    __all__.append(p)

for p in __all__:
    _imported_vehicle = importlib.import_module(f"road_vehicle.vehicles.lorries.{p}")
    setattr(module, p, _imported_vehicle.the_variant)
    del _imported_vehicle
