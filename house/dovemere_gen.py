#!/usr/bin/env python
import grf


def main():
    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bh",
        name="Ahyangyi's Dovemere Houses",
        description="A house set modeled after buildings in Wuhu, Anhui, China.",
        id_map_file="house/id_map.json",
        sprite_cache_path="house/.cache",
    )

    g.add_int_parameter(
        name="Vanilla houses",
        description="Whether to disable vanilla houses",
        default=0,
        limits=(0, 1),
        enum={0: "Disabled", 1: "Enabled"},
    )
    g.add(grf.If(is_static=True, variable=0, condition=0x02, value=1, skip=1, varsize=4))
    g.add(grf.DefineMultiple(feature=grf.HOUSE, first_id=0, props={"substitute": [0xFF] * 0x6E}))

    import house.houses.dovemere_gable

    g.add(house.houses.dovemere_gable.the_house)

    g.write("house.grf")


if __name__ == "__main__":
    main()
