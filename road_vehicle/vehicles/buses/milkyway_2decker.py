from datetime import date
from road_vehicle.lib import ABus
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel
from agrf.variant import AVariant
import cargos


variant = AVariant(
    id=0x1050,
    name="Milky Way Double-Decker Bus",
    introduction_date=date(2014, 1, 1),
    vehicle_life=15,
    model_life=127,
    max_speed=ABus.kmh(80),
    power=ABus.hp(240),
    weight=12,
    techclass="2decker",
    cargo_capacity=100,
    default_cargo_type=0,
    tags={"air conditioner"},
    graphics_helper=AutoWolf("placeholder"),
    real_class=ABus,
)
