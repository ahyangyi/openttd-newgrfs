from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.variant import AVariant


variant = AVariant(
    real_class=ABus,
    id=0x1004,
    name="Longriver Coach",
    translation_name="LONGRIVER_COACH",
    introduction_date=date(1980, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(75),
    power=ABus.hp(134),
    full_weight=9.9,
    techclass="coach",
    cargo_capacity=47,
    real_dimensions=(9.50, 2.48, 2.95),
    real_x_dimensions=(1.51, 5, 2.99),
    axle_track=(1.91, 1.80),
    tire=StandardProfileRadialTire(11, 20),  # No data
    graphics_helper=AutoWolf("longriver"),
)
