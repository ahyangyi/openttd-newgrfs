from datetime import date
from road_vehicle.lib import ALorry, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.variant import AVariant


the_variant = AVariant(
    real_class=ALorry,
    id=0x2100,
    name="Happyone Truck",
    translation_name="HAPPYONE",
    introduction_date=date(1940, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ALorry.kmh(80),
    power=ALorry.hp(95),
    weight=4.2,
    tags=["sanctioned"],
    techclass="l_truck",
    cargo_capacity=3,
    default_cargo_type=0,
    real_dimensions=(5.518, 2.286, 3.048),
    axle_track=(1.791, 1.753),
    real_x_dimensions=(0.965, 3.41, 1.143),
    tire=BiasPlyTire(10.5, 20),
    graphics_helper=AutoWolf("happyone"),
)
