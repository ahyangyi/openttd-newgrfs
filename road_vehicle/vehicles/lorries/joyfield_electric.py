from datetime import date
from road_vehicle.lib import ALorry, StandardProfileRadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle


the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x2218,
    translation_name="JOYFIELD_ELECTRIC_LORRY",
    introduction_date=date(2018, 1, 1),
    vehicle_life=15,
    model_life=20,
    max_speed=ALorry.kmh(95),
    power=ALorry.kW(100),
    weight=3.22,
    techclass="l_truck",
    cargo_capacity=3,  # 3.08
    default_cargo_type=0,
    real_dimensions=(5.995, 2.16, 3.18),
    tire=StandardProfileRadialTire(12, 22.5),  # FIXME
    graphics_helper=AutoWolf("placeholder"),
)
