from datetime import date
from road_vehicle.lib import ABus, RadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1231,
    translation_name="JOYFIELD_ARTICULATED",
    introduction_date=date(2020, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(75),  # N/A
    power=ABus.kW(118),
    weight=18,
    techclass="bus",
    cargo_capacity=125,
    real_dimensions=(16.5, 2.55, 3.26),
    tire=RadialTire(275, 70, 22.5),
    graphics_helper=AutoWolf("placeholder"),
)
