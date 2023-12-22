from datetime import date
from road_vehicle.lib import ABus, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x3000,
    translation_name="BURGER",
    introduction_date=date(1957, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(55),  # No data
    power=ABus.hp(95),
    weight=5.0,
    techclass="trolleybus",
    cargo_capacity=80,
    graphics_helper=AutoWolf("placeholder"),
)
