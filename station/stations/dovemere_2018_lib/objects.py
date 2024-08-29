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
)
