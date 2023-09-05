from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date
import grf


the_road = ARoadType(
    id=0x01,
    name="Slate Block Road",
    label=b"SLAT",
    introduction_date=date(170, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    translation_name="SLATE_BLOCK",
)
