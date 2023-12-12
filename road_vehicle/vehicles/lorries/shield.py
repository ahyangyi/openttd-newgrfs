from datetime import date
from road_vehicle.lib import ALorry, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x2200,
    translation_name="SHIELD",
    introduction_date=date(2010, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ALorry.kmh(110),
    power=ALorry.hp(580),
    weight=8.3,
    techclass="h_truck",
    cargo_capacity=40,
    default_cargo_type=0,
    real_dimensions=(6.873, 2.55, 3.79),
    real_x_dimensions=(1.48, 3.3, 1.35, 0.743),
    axle_track=(2.04, 1.86, 1.86),
    tire=StandardProfileRadialTire(12, 22.5),
    graphics_helper=AutoWolf("shield"),
)
