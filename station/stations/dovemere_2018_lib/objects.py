import grf
from grfobject.lib import AObject
from station.lib import ALayout
from .layouts import solid_ground

test_layout = ALayout(solid_ground, [], True)
test_object = AObject(
    id=0x0,
    translation_name="STRAIGHT_STAIR",
    layouts=[test_layout, test_layout.T],
    class_label=b"\xe8\x8a\x9cZ",
    climates_available=grf.ALL_CLIMATES,
    size=(1, 1),
    num_views=4,
    introduction_date=0,
    end_of_life_date=0,
    height=1,
    flags=grf.Object.Flags.ONLY_IN_GAME,
)
