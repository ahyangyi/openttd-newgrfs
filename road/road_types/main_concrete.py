from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date


the_road_type = ARoadType(
    id=0x05,
    name="Main Road (Concrete)",
    label=b"CON3",
    introduction_date=date(1940, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    translation_name="MAIN_CONCRETE",
)
