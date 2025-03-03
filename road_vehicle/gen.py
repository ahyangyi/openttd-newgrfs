#!/usr/bin/env python
from road_vehicle.rosters import everything, city_rosters
from cargos import cargos
import argparse
import grf
import struct


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("road_vehicle/lang", default_lang_file="english-uk.lng")
    return s


def gen(fast):
    s = get_string_manager()

    g = grf.NewGRF(
        grfid=b"\xe5\xbc\x8b0",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="road_vehicle/id_map.json",
        sprite_cache_path="road_vehicle/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    from road_vehicle.lib.parameters import parameter_list

    parameter_list.add(g, s)

    # Parameter 0
    g.add(
        grf.If(is_static=True, variable=parameter_list.index("VANILLA_RV"), condition=0x02, value=1, skip=1, varsize=4)
    )
    g.add(grf.DisableDefault(grf.RV, range(88)))

    # Parameter 1
    nightgfx_id = struct.unpack("<I", b"\xffOTN")[0]
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=1))
    g.add(grf.If(is_static=False, variable=0x88, condition=0x06, value=nightgfx_id, skip=1, varsize=4))
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=0))

    g.set_cargo_table(cargos)
    g.add(grf.BaseCosts({grf.BaseCosts.BUILD_VEHICLE_ROAD: 9, grf.BaseCosts.RUNNING_ROADVEH: 9}))

    # Put a permanent empty sprite at 31
    for feature in [grf.RV, grf.TRAIN]:
        g.add(grf.Action1(feature=feature, first_set=31, set_count=1, sprite_count=8))
        for _ in range(8):
            g.add(grf.EMPTY_SPRITE)

    everything.register(g)
    g.write("road_vehicle.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen(args.fast)
    elif args.cmd == "doc":
        from road_vehicle.docgen import gen_docs

        gen_docs(get_string_manager(), city_rosters, everything)
    else:
        print("\n" + everything.cli())


if __name__ == "__main__":
    main()
