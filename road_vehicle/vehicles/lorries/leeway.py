from datetime import date
from road_vehicle.lib import ALorry
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x2300,
    translation_name="LEEWAY",
    introduction_date=date(1942, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ALorry.kmh(64),
    power=ALorry.hp(118),
    weight=4.5,
    tags=["sanctioned"],
    techclass="l_truck",
    cargo_capacity=3,
    default_cargo_type=0,
    graphics_helper=AutoWolf("happyone"),
)
