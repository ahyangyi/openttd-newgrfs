from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date


the_road_type = ARoadType(
    id=0x10,
    name="Motorway",
    label=b"MTWY",
    introduction_date=date(1980, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    translation_name="MOTORWAY",
)
