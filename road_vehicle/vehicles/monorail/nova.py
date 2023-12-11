from datetime import date
from road_vehicle.lib import AMonorail
from road_vehicle.lib.graphics.voxel import LazyVoxel
from road_vehicle.lib.graphics.autowolf import AutoWolf
from agrf.metavehicle import AMetaVehicle
from train.lib import ATrain
import grf


nova = LazyVoxel("nova", config={"agrf_unnaturalness": 1})

nova_f = LazyVoxel("nova_f", config={"agrf_unnaturalness": 1})

the_variant = AMetaVehicle(
    id=0x3000,
    name="Nova",
    translation_name="NOVA",
    introduction_date=date(2010, 1, 1),
    vehicle_life=30,
    model_life=40,
    max_speed=AMonorail.kmh(90),
    power=AMonorail.kW(310),
    weight=14,
    techclass="monorail",
    cargo_capacity=198,
    default_cargo_type=0,
    tractive_effort_coefficient=178,
    # real_dimensions=(13.21, 3.147, 4.046),
    graphics_helper=AutoWolf(
        [nova_f, nova, nova, (nova_f, "rotate")],
        lengths=[1, 1, 8, 1, 1, 1, 8, 1, 1, 8, 1, 1, 1, 8, 1, 1],
        segments=[
            None,
            None,
            (0, 11),
            None,
            None,
            None,
            (12, 21),
            None,
            None,
            (22, 31),
            None,
            None,
            None,
            (32, 43),
            None,
            None,
        ],
        flags=("noflipY",),
    ),
    real_class=AMonorail,
    variants=[
        dict(
            real_class=ATrain,
            id=0x3001,
            name="Nova",
            track_type=1,
            max_speed=90,
            power=AMonorail.kW(15000),
            engine_class=grf.Train.EngineClass.MONORAIL,
        )
    ],
)
