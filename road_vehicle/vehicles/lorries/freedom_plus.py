from datetime import date
from road_vehicle.lib import ALorry
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x20C0,
    introduction_date=date(1982, 1, 1),
    vehicle_life=15,
    model_life=15,
    max_speed=ALorry.kmh(75),
    power=ALorry.hp(100),
    weight=3.9,
    techclass="l_truck",
    cargo_capacity=4.5,
    default_cargo_type=0,
    real_dimensions=(6.66, 2.46, 2.2),
    voxel_dimensions=(148, 68, 48),
    axle_track=(1.70, 1.74),
    real_x_dimensions=(0.874, 4.00, 1.786),
    graphics_helper=AutoWolf("placeholder"),
)
