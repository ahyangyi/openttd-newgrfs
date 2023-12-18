from road.lib import ATramType
from road.lib.graphics.underlay import get_spritesheet
from datetime import date


the_tram_type = ATramType(
    id=0x11,
    name="Monorail",
    label=b"MONO",
    introduction_date=date(1953, 1, 1),
    underlay=get_spritesheet("wolf_a"),
    overlay=get_spritesheet("monorail"),
    translation_name="MONORAIL",
)
