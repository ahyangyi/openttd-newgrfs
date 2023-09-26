from industry.lib.economy import Economy, PrimaryIndustry, SecondaryIndustry, TertiaryIndustry, Town
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
    diamond_mine,
    towns,
)


the_economy = Economy(
    name="Vanilla Sub-Tropic",
    graph={
        copper_ore_mine: PrimaryIndustry(copper_ore),
        oil_wells: PrimaryIndustry(oil),
        diamond_mine: PrimaryIndustry(diamonds),
        farm: PrimaryIndustry(maize),
        lumber_mill: PrimaryIndustry(wood),
        fruit_plantation: PrimaryIndustry(fruit),
        rubber_plantation: PrimaryIndustry(rubber),
        food_processing_plant: SecondaryIndustry((fruit, maize), food),
        oil_refinery: SecondaryIndustry(oil, goods),
        factory: SecondaryIndustry((rubber, copper_ore, wood), goods),
        bank: TertiaryIndustry(diamonds),
        towns: Town(passengers, mail, food, goods),
    },
)
