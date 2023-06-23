#!/usr/bin/env python
import grf

g = grf.NewGRF(
    grfid=b"\xE5\xBC\x8Bb",
    name="Ahyangyi's Dovemere Bridges",
    description="TBD.",
    id_map_file="bridge/id_map.json",
    sprite_cache_path="bridge/.cache",
)

g.write("bridge.grf")
