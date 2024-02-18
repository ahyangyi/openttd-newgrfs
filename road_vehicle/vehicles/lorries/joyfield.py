from datetime import date
from road_vehicle.lib import ALorry, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x2210,
    translation_name="JOYFIELD_LORRY",
    introduction_date=date(2012, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ALorry.kmh(110),
    power=ALorry.hp(560),
    weight=8.5,
    techclass="h_truck",
    cargo_capacity=40,
    default_cargo_type=0,
    real_dimensions=(6.965, 2.525, 3.73),
    real_x_dimensions=(1.46, 3.3, 1.35, 0.855),
    axle_track=(2.05, 1.865, 1.88),
    tire=StandardProfileRadialTire(12, 22.5),
    graphics_helper=AutoWolf("shield"),
)
