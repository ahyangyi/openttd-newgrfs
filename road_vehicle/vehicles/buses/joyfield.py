from datetime import date
from road_vehicle.lib import ABus, RadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1230,
    translation_name="JOYFIELD",
    introduction_date=date(2017, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(80),  # data from older model
    power=ABus.kW(160),
    weight=13.3,
    techclass="bus",
    cargo_capacity=72,
    real_dimensions=(12.0, 2.55, 3.25),
    real_x_dimensions=(2.67, 5.90, 3.43),
    axle_track=(2.098, 1.840),
    tire=RadialTire(275, 70, 22.5),
    graphics_helper=AutoWolf("placeholder"),
)
