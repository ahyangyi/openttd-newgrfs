from datetime import date
from road_vehicle.lib import ABus, RadialTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel
from agrf.variant import AVariant
import cargos


the_variant = AVariant(
    id=0x1030,
    name="Raregem Bus",
    translation_name="RAREGEM",
    introduction_date=date(2020, 1, 1),
    vehicle_life=15,
    model_life=127,
    max_speed=ABus.kmh(90),
    power=ABus.kW(156),
    weight=11.55,
    techclass="bus",
    cargo_capacity=70,
    real_dimensions=(10.58, 2.50, 3.41),
    real_x_dimensions=(2.11, 5.25, 3.22),
    axle_track=(2.09, 1.88),
    voxel_dimensions=(230, 72, 74),
    tire=RadialTire(275, 70, 22.5),
    tags={"air conditioner"},
    graphics_helper=AutoWolf("raregem"),
    real_class=ABus,
    variants=[
        dict(id=0x1031, variant_group=0x1030, extra_flags=0xB, graphics_helper=AutoWolf("raregem03")),
        # XXX
        dict(
            id=0x1032,
            name="Raregem Bus - Night Test",
            variant_group=0x1030,
            extra_flags=0xB,
            graphics_helper=AutoWolf(LazyVoxel("raregem").self_compose("night_lights", colour_map=cargos.NIGHT)),
        ),
    ],
)
