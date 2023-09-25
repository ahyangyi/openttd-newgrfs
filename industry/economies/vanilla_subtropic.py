from industry.lib.economy import Economy
from industry.cargos import (
    copper_ore,
    food,
    goods,
    diamonds,
    livestock,
    mail,
    oil,
    paper,
    passengers,
    maize,
    wood,
)
from industry.industries import (
    bank,
    copper_ore_mine,
    food_processing_plant,
    farm,
    lumber_mill,
    paper_mill,
    oil_refinery,
    printing_works,
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
                livestock,
                maize,
            ),
            food,
        ),
        farm: ((), maize),
        lumber_mill: ((), wood),
        paper_mill: (wood, paper),
        oil_refinery: (oil, goods),
        printing_works: (paper, goods),
        oil_wells: ((), oil),
        power_station: (copper_ore, ()),
        diamond_mine: ((), diamonds),
    },
    town_industries=(passengers, mail, food, goods),
)
