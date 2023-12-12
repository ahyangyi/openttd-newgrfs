from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x100C,
    translation_name="LONGRIVER_2DECKER",
    introduction_date=date(1995, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ABus.kmh(75),
    power=ABus.kW(192),
    weight=10.6,
    techclass="2decker",
    cargo_capacity=90,
    real_dimensions=(10.49, 2.48, 4.18),
    real_x_dimensions=(2.32, 5.00, 3.17),
    axle_track=(2.02, 1.86),
    tire=StandardProfileRadialTire(11, 20),
    graphics_helper=AutoWolf("longriver_2decker"),
)
