from datetime import date
from road_vehicle.lib import ABus, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    id=0x1010,
    name="Happyone Bus",
    translation_name="HAPPYONE_BUS",
    introduction_date=date(1940, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(65),
    power=ABus.hp(95),
    weight=4.5,
    tags={"sanctioned"},
    techclass="bus",
    cargo_capacity=45,
    real_dimensions=(6, 2.50, 3),
    axle_track=(1.791, 1.753),
    tire=BiasPlyTire(10.5, 20),
    graphics_helper=AutoWolf("happyone"),
    real_class=ABus,
)
