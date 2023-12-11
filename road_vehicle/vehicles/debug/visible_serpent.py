from datetime import date
from road_vehicle.lib import ABus
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


length = 128

the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x3FFF,
    name="Visible Snake",
    introduction_date=date(1900, 1, 1),
    vehicle_life=255,
    model_life=255,
    max_speed=ABus.kmh(15),
    power=ABus.hp(100),
    weight=5,
    cargo_capacity=12,
    default_cargo_type=0,
    graphics_helper=AutoWolf(
        ["bounding_box_2d"] * length,
        lengths=[1] * length,
        segments=[(i, i + 1) for i in range(length)],
        flags=["debug_bbox"],
    ),
)
