#!/usr/bin/env python
import grf


def main():
    s = grf.StringManager()
    s.import_lang_dir("bridge/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bb",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="bridge/id_map.json",
        sprite_cache_path="bridge/.cache",
        bpp=32,
    )

    from bridge.bridges import test

    g.add(test.the_bridge)

    g.write("bridge.grf")


if __name__ == "__main__":
    main()
