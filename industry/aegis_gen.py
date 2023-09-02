#!/usr/bin/env python
import grf


def main():
    s = grf.StringManager()
    s.import_lang_dir("industry/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bi",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="industry/id_map.json",
        bpp=32,
    )

    g.write("aegis.grf")


if __name__ == "__main__":
    main()
