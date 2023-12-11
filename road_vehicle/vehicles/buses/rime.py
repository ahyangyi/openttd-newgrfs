from datetime import date
from road_vehicle.lib import ABus, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1040,
    name="Rime Bus",
    translation_name="RIME",
    introduction_date=date(1957, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(55),  # No data
    power=ABus.hp(95),
    weight=5.0,
    techclass="bus",
    cargo_capacity=80,
    real_dimensions=(8.2, 2.5, 3.05),  # No data for width/height, using BK640
    real_x_dimensions=(0, 4.46, 0),  # No data, using BK640
    axle_track=(1.70, 1.74),  # No data, using CA10
    tire=BiasPlyTire(9, 20),  # No data, using CA10
    graphics_helper=AutoWolf("placeholder"),
)
