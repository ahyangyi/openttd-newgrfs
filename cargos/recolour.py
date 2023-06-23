from .cargos import cargo_info
from agrf.graphics.recolour import ColourRange, ColourMap

coal_remaps = {k: v["COAL"] for k, v in cargo_info.items() if "COAL" in v}

NIGHT = ColourMap(
    "night",
    [(ColourRange(131, 137), ColourRange(246, 246))],
)
