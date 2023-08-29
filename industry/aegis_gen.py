#!/usr/bin/env python
import grf


def main():
    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bi",
        name="Ahyangyi's Extended Generic Industry Set",
        description="Industry sets with options to support various playstyles.",
        id_map_file="industry/id_map.json",
    )

    g.write("aegis.grf")


if __name__ == "__main__":
    main()
