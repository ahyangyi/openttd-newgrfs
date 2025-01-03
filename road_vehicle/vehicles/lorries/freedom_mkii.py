from datetime import date
from road_vehicle.lib import ALorry, BiasPlyTire
from road_vehicle.lib.graphics.autowolf import AutoWolf
from road_vehicle.lib.graphics.voxel import LazyVoxel, LazyAlternatives
from agrf.metavehicle import AMetaVehicle
import cargos
from agrf.graphics.recolour import *
from agrf.magic import Switch

lowside = LazyVoxel("freedom").compose("road_vehicle/voxels/parts/open.vox", "open")

empty = lowside.produce_empty("empty")
coal = lowside.compose("road_vehicle/voxels/parts/cargo/coal.vox", "coal")

lowside_switch = Switch(
    ranges={
        cargos.cargos.index(k): LazyAlternatives(
            (empty, lowside.compose("road_vehicle/voxels/parts/cargo/coal.vox", v.name, colour_map=v))
        )
        for k, v in cargos.coal_remaps.items()
    },
    default=LazyAlternatives((empty, coal)),
    code="cargo_type_in_veh",
)

the_variant = AMetaVehicle(
    real_class=ALorry,
    id=0x2080,
    translation_name="FREEDOM_MK_II",
    introduction_date=date(1983, 1, 1),
    vehicle_life=15,
    model_life=15,
    max_speed=ALorry.kmh(80),
    power=ALorry.hp(115),
    weight=3.9,
    techclass="l_truck",
    cargo_capacity=5,
    default_cargo_type=0,
    real_dimensions=(6.855, 2.46, 2.2),
    axle_track=(1.70, 1.74),
    real_x_dimensions=(0.874, 4.175, 1.806),
    tire=BiasPlyTire(9, 20),
    graphics_helper=AutoWolf(lowside_switch, flags=("noflipY",)),
)
