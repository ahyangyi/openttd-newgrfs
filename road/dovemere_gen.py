#!/usr/bin/env python
import grf


def main():
    s = grf.StringManager()
    s.import_lang_dir("road/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Br",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="road/id_map.json",
        sprite_cache_path="road/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )
    from road.road_types import slate_block, main_asphalt, highway

    g.add(slate_block.the_road)
    g.add(main_asphalt.the_road)
    g.add(highway.the_road)

    g.write("road.grf")


if __name__ == "__main__":
    main()
