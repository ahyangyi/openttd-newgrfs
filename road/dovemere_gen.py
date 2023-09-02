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
        bpp=32,
    )
    import road.road_types.slate_block
    import road.road_types.wolf_a

    g.add(road.road_types.slate_block.the_road)
    g.add(road.road_types.wolf_a.the_road)

    g.write("road.grf")


if __name__ == "__main__":
    main()
