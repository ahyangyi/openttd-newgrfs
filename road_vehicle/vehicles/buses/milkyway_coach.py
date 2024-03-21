from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1094,
    translation_name="MILKYWAY_COACH",
    introduction_date=date(2012, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(110),  # Based on various export models
    power=ABus.hp(220),
    weight=8.61,
    techclass="coach",
    cargo_capacity=45,
    real_dimensions=(8.774, 2.47, 3.385),
    real_x_dimensions=(1.814, 4.25, 2.71),
    axle_track=(2.02, 1.80),
    tire=StandardProfileRadialTire(9, 22.5),
    graphics_helper=AutoWolf("placeholder"),
)
