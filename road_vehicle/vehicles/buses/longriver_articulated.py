from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.variant import AVariant


variant = AVariant(
    id=0x1008,
    name="Longriver Articulated Bus",
    introduction_date=date(1980, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(65),
    power=ABus.hp(134),
    weight=10.10,
    techclass="articulated_bus",
    tractive_effort_coefficient=53,
    cargo_capacity=130,
    real_dimensions=(14.74, 2.48, 2.95),
    real_x_dimensions=(1.51, 4.7, 5.54, 2.99),
    axle_track=(1.91, 1.80),
    tire=StandardProfileRadialTire(11, 20),  # No data
    graphics_helper=AutoWolf(
        name=("longriver_articulated_f", "longriver_articulated_b"),
        lengths=(1, 1, 5, 1, 1, 1, 1, 1, 1),
        segments=(None, None, (0, 6), None, (8, 12), None, None, None, None),
    ),
    real_class=ABus,
)
