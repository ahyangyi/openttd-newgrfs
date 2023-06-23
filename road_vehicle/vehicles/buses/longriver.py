from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.variant import AVariant


variant = AVariant(
    real_class=ABus,
    id=0x1000,
    name="Longriver Bus",
    introduction_date=date(1980, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(70),
    power=ABus.hp(134),
    full_weight=11.58,
    techclass="bus",
    cargo_capacity=85,
    default_cargo_type=0,
    additional_text="Longriver company was the first one to build buses on a custom chassis instead of modifying Freedom trucks. It was hugely popular in the 1980s and 1990s.",
    real_dimensions=(9.20, 2.48, 2.95),
    voxel_dimensions=(200, 72, 64),
    real_x_dimensions=(1.51, 4.7, 2.99),
    axle_track=(1.91, 1.80),
    tire=StandardProfileRadialTire(11, 20),  # No data
    graphics_helper=AutoWolf("longriver"),
)
