from industry.lib.economy import Economy
from industry.cargos import (
    copper_ore,
    food,
    goods,
    diamonds,
    mail,
    oil,
    passengers,
    maize,
    wood,
    fruit,
    rubber,
)
from industry.industries import (
    bank,
    copper_ore_mine,
    food_processing_plant,
    farm,
    lumber_mill,
    fruit_plantation,
    rubber_plantation,
    oil_refinery,
    factory,
    oil_wells,
    power_station,
    diamond_mine,
)


the_economy = Economy(
    name="Vanilla Sub-Tropic",
    graph={
        bank: (diamonds, ()),
        copper_ore_mine: ((), copper_ore),
        food_processing_plant: (
            (
                fruit,
                maize,
            ),
            food,
        ),
        farm: ((), maize),
        lumber_mill: ((), wood),
        fruit_plantation: ((), fruit),
        rubber_plantation: ((), rubber),
        oil_refinery: (oil, goods),
        factory: ((rubber, copper_ore, wood), goods),
        oil_wells: ((), oil),
        power_station: (copper_ore, ()),
        diamond_mine: ((), diamonds),
    },
    town_cargos=(passengers, mail, food, goods),
)
