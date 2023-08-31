from datetime import date
from road_vehicle.lib import ALorry, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel, LazyAlternatives, LazySwitch
from agrf.variant import AVariant

import cargos

lowside = LazyVoxel(
    "freedom",
).compose(
    "road_vehicle/voxels/parts/open.vox",
    "open",
)

empty = lowside.produce_empty("empty")
coal = lowside.compose(
    "road_vehicle/voxels/parts/cargo/coal.vox",
    "coal",
)

lowside_switch = LazySwitch(
    ranges={
        cargos.cargos.index(k): LazyAlternatives(
            (
                empty,
                lowside.compose(
                    "road_vehicle/voxels/parts/cargo/coal.vox",
                    v.name,
                    colour_map=v,
                ),
            )
        )
        for k, v in cargos.coal_remaps.items()
    },
    default=LazyAlternatives((empty, coal)),
    code="cargo_type_in_veh",
)

variant = AVariant(
    id=0x2000,
    name="Freedom Open Truck",
    translation_name="FREEDOM",
    additional_text="A very versatile military truck, but also widely used for civilian purposes.",
    introduction_date=date(1956, 7, 13),
    vehicle_life=15,
    model_life=30,
    max_speed=ALorry.kmh(65),
    power=ALorry.hp(95),
    weight=3.9,
    techclass="l_truck",
    cargo_capacity=4,
    default_cargo_type=0,
    refittable_cargo_classes=cargos.OPEN_CARGO_CLASSES,
    real_dimensions=(6.72, 2.385, 2.180),
    voxel_dimensions=(146, 70, 48),
    axle_track=(1.70, 1.74),
    real_x_dimensions=(0.874, 4.00, 1.786),
    tire=BiasPlyTire(9, 20),
    real_class=ALorry,
    graphics_helper=AutoWolf(
        lowside_switch,
        flags=("noflipY",),
    ),
    variants=[
        dict(
            id=0x2001,
            name="Freedom Tanker",
            translation_name="FREEDOM_TANKER",
            refittable_cargo_classes=cargos.TANKER_CARGO_CLASSES,
            graphics_helper=AutoWolf(
                LazyVoxel(
                    "freedom",
                ).compose(
                    "road_vehicle/voxels/parts/tanker.vox",
                    "tanker",
                ),
                flags=("noflipY",),
            ),
        ),
        dict(
            id=0x2002,
            name="Freedom Tarpaulin Truck",
            translation_name="FREEDOM_TARPAULIN",
            refittable_cargo_classes=cargos.TARPAULIN_CARGO_CLASSES,
            graphics_helper=AutoWolf(
                LazyVoxel(
                    "freedom",
                ).compose(
                    "road_vehicle/voxels/parts/tarpaulin.vox",
                    "tarpaulin",
                ),
                flags=("noflipY",),
            ),
        ),
    ],
)
