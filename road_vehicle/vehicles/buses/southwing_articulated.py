from datetime import date
from road_vehicle.lib import ABus, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1070,
    translation_name="SOUTHWING_ARTICULATED",
    introduction_date=date(1959, 8, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(50),  # No data
    power=ABus.hp(95),
    weight=9.0,
    techclass="articulated_bus",
    cargo_capacity=135,
    real_dimensions=(13.7, 2.5, 3.05),  # No data
    real_x_dimensions=(0, 4.46, 0),  # No data
    axle_track=(1.70, 1.74),  # No data, using CA10
    tire=BiasPlyTire(9, 20),  # No data, using CA10
    graphics_helper=AutoWolf("placeholder"),
)
