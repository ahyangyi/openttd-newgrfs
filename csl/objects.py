from station.lib import BuildingFull, BuildingSymmetricalX, ALayout
from .grounds import named_grounds
from .components import components
from ..objects_utils import named_layouts, register

def make_objects():
    layout = ALayout(None, components.tiny, False, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "decorated")] = layout
    register([[layout]], BuildingFull, b"L", starting_id=0x0200)
