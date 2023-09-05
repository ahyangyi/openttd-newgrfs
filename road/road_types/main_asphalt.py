from road.lib import ARoadType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date
import grf


the_road = ARoadType(
    id=0x04,
    name="Main Road (Asphalt)",
    label=b"ASP3",
    introduction_date=date(1940, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    toolbar_caption="Main Road (Asphalt) Construction",
    menu_text="Main Road (Asphalt) Construction",
)
