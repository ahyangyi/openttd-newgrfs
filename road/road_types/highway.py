from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date
import grf


the_road = ARoadType(
    id=0x10,
    name="Highway",
    label=b"HIWY",
    introduction_date=date(1980, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    translation_name="HIGHWAY",
)
