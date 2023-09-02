from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date
import grf


the_road = ARoadType(
    id=0x01,
    name="Wolf A",
    label=b"WOLF",
    introduction_date=date(1920, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    toolbar_caption="Wolf A Road",
)
