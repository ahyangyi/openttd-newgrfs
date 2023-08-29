#!/usr/bin/env python
import road_vehicle.rosters.dovemere as dovemere
from cargos import cargos
import argparse
import grf
import struct


def gen(fast):
    s = grf.StringManager()
    s.import_lang_dir("road_vehicle/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8B0",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="road_vehicle/id_map.json",
        sprite_cache_path="road_vehicle/.cache",
        strings=s,
    )

    # Parameter 0
    g.add_int_parameter(
        name=s["STR_PARAM_VANILLA_RV"],
        description=s["STR_PARAM_VANILLA_RV_DESC"],
        default=0,
        limits=(0, 1),
        enum={0: "Disabled", 1: "Enabled"},
    )
    g.add(grf.If(is_static=True, variable=0, condition=0x02, value=1, skip=1, varsize=4))
    g.add(grf.DefineMultiple(feature=grf.RV, first_id=0, props={"climates_available": [0] * 88}))

    # Parameter 1
    g.add_int_parameter(
        name=s["STR_PARAM_NIGHT_MODE"],
        description=s["STR_PARAM_NIGHT_MODE_DESC"],
        default=0,
        limits=(0, 2),
        enum={0: "Auto-Detect", 1: "Enabled", 2: "Disabled"},
    )
    nightgfx_id = struct.unpack("<I", b"\xffOTN")[0]
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=1))
    g.add(grf.If(is_static=False, variable=0x88, condition=0x06, value=nightgfx_id, skip=1, varsize=4))
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=0))

    g.set_cargo_table(cargos)
    g.add(grf.BaseCosts({grf.BaseCosts.BUILD_VEHICLE_ROAD: 9, grf.BaseCosts.RUNNING_ROADVEH: 9}))

    # Put a permanent empty sprite at 31
    for feature in [grf.RV, grf.TRAIN]:
        g.add(
            grf.Action1(
                feature=feature,
                first_set=31,
                set_count=1,
                sprite_count=8,
            )
        )
        for _ in range(8):
            g.add(grf.EMPTY_SPRITE)

    dovemere.roster.register(g)
    g.write("road_vehicle.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen(args.fast)
    else:
        print("\n" + dovemere.roster.cli())


if __name__ == "__main__":
    main()
