from datetime import date
from road_vehicle.lib import ABus, RadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel
from agrf.variant import AVariant
import cargos


variant = AVariant(
    id=0x1050,
    name="Milky Way Double-Decker Bus",
    translation_name="MILKYWAY_2DECKER",
    introduction_date=date(2014, 1, 1),
    vehicle_life=15,
    model_life=127,
    max_speed=ABus.kmh(85),
    power=ABus.hp(240),
    weight=12,
    techclass="2decker",
    cargo_capacity=95,
    real_dimensions=(11.31, 2.55, 4.14),
    real_x_dimensions=(2.548, 5.500, 3.262),
    axle_track=(2.063, 1.860),
    tire=RadialTire(275, 70, 22.5),
    tags={"air conditioner"},
    graphics_helper=AutoWolf("milkyway_2decker"),
    real_class=ABus,
)
