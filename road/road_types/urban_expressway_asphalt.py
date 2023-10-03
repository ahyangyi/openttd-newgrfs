from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date
import grf


the_road_type = ARoadType(
    id=0x05,
    name="Urban Expressway (Asphalt)",
    label=b"UREA",
    introduction_date=date(1970, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    translation_name="URBAN_EXPRESSWAY",
)
