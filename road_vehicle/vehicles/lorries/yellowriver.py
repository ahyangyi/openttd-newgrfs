from datetime import date
from road_vehicle.lib import ALorry, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel
from agrf.metavehicle import AMetaVehicle
import cargos
from agrf.graphics.recolour import *

the_variant = AMetaVehicle(
    id=0x2300,
    name="Yellow River Truck",
    translation_name="YELLOWRIVER",
    introduction_date=date(1960, 4, 15),
    vehicle_life=15,
    model_life=30,
    max_speed=ALorry.kmh(60),
    power=ALorry.kW(103),
    weight=6.8,
    techclass="h_truck",
    cargo_capacity=8,
    default_cargo_type=0,
    real_dimensions=(7.6, 2.4, 2.6),
    axle_track=(1.927, 1.751),  # Škoda 706 RT values
    real_x_dimensions=(1.4, 4.0, 2.2),
    tire=BiasPlyTire(11, 20),
    refittable_cargo_classes=cargos.OPEN_CARGO_CLASSES,
    real_class=ALorry,
    graphics_helper=AutoWolf(LazyVoxel("yellowriver"), flags=("noflipY",)),
)
