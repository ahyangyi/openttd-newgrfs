from agrf.lib.building.layout import ADefaultGroundSprite, ALayout
from station.lib import AStation, AMetaStation
from station.lib.registers import Registers, code

concrete_ground = ALayout(ADefaultGroundSprite(1420, flags={"add": Registers.ZERO}), [], False)

station = AStation(
    id=0x0000,
    translation_name="CONCRETE_GROUND",
    layouts=[concrete_ground] * 2,
    class_label=b"\xe5\xbc\x8bf",
    non_traversable_tiles=0b11,
    doc_layout=concrete_ground,
    extra_code=code,
    callbacks={"select_tile_layout": 0},
)


ground_stations = AMetaStation([station], b"\xe5\xbc\x8bf", [b"\xe5\xbc\x8bf"], [])
