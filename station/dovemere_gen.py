#!/usr/bin/env python
import grf


def main():
    s = grf.StringManager()
    s.import_lang_dir("station/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bs",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="station/id_map.json",
        sprite_cache_path="station/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    import station.stations.dovemere_2018
    import station.stations.dovemere_1992

    for station in station.stations.dovemere_2018.the_stations:
        g.add(station)
    # g.add(station.stations.dovemere_1992.the_station)

    g.write("station.grf")


if __name__ == "__main__":
    main()
