from datetime import date
from road_vehicle.lib import ABus, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ABus,
    id=0x1068,
    translation_name="NORTHWING_ARTICULATED",
    introduction_date=date(1979, 1, 1),
    vehicle_life=15,
    model_life=30,
    max_speed=ABus.kmh(65),
    power=ABus.kW(132),
    weight=13.29,
    techclass="articulated_bus",
    cargo_capacity=200,
    real_dimensions=(16.82, 2.5, 3.05),
    real_x_dimensions=(0, 5.5, 6.255, 0),
    axle_track=(1.927, 1.751, 1.751),  # Škoda 706 RT values
    tire=StandardProfileRadialTire(11, 20),
    graphics_helper=AutoWolf("placeholder"),
)
