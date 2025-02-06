from industry.lib.economy import (
    MetaEconomy,
    Economy,
    PrimaryIndustry,
    FreePort,
    SecondaryIndustry,
    TertiaryIndustry,
    Town,
)
from industry.cargos import (
    ammonia,
    china_clay,
    engineering_supplies,
    explosives,
    farm_supplies,
    fertiliser,
    fish,
    food,
    mail,
    paper,
    passengers,
    peat,
    phosphate,
    potash,
    pyrite_ore,
    sulphur,
    timber,
    water,
    wood,
    zinc,
)
from industry.industries import (
    ashery,
    ammonia_plant,
    chemical_plant,
    clay_pit,
    fish_farm,
    fishing_grounds,
    fishing_harbor,
    forest,
    general_store,
    herding_coop,
    paper_mill,
    peatlands,
    phosphate_mine,
    port,
    power_station,
    pyrite_mine,
    pyrite_smelter,
    sawmill,
    towns,
    trading_centre,
    water_supply,
    water_tower,
    wharf,
)


class TheEconomy(MetaEconomy):
    def __init__(self):
        super().__init__("BASIC_ARCTIC")

    def get_economy(self, parameters):
        ret = Economy(
            {
                clay_pit: PrimaryIndustry(china_clay),
                peatlands: PrimaryIndustry(peat),
                phosphate_mine: PrimaryIndustry(phosphate),
                pyrite_mine: PrimaryIndustry(pyrite_ore),
                fish_farm: PrimaryIndustry(fish),
                fishing_grounds: PrimaryIndustry(fish),
                forest: PrimaryIndustry(wood),
                herding_coop: PrimaryIndustry(food),
                ammonia_plant: SecondaryIndustry(peat, ammonia),
                ashery: SecondaryIndustry(wood, potash),
                chemical_plant: SecondaryIndustry((phosphate, sulphur, ammonia, potash), (explosives, fertiliser)),
                fishing_harbor: SecondaryIndustry(fish, food),
                paper_mill: SecondaryIndustry((wood, sulphur, china_clay), paper),
                pyrite_smelter: SecondaryIndustry(pyrite_ore, (sulphur, zinc)),
                sawmill: SecondaryIndustry(wood, timber),
                power_station: TertiaryIndustry(peat),
                general_store: TertiaryIndustry((explosives, fertiliser, zinc, timber)),
                towns: Town(passengers, mail, food, paper),
            },
            parameters,
        )
        if parameters["POLICY"] == "SELF_SUFFICIENT":
            ret.graph[port] = FreePort((zinc, fertiliser, paper), (china_clay, ammonia))
            ret.graph[wharf] = FreePort((peat, timber, explosives), potash)
            del ret.graph[general_store]  # FIXME
        elif parameters["POLICY"] in ("FREE_TRADE", "EXPORT"):
            ret.graph[port] = FreePort((zinc, fertiliser, paper), (china_clay, ammonia))
            ret.graph[wharf] = FreePort((peat, timber, explosives), potash)
            del ret.graph[general_store]  # FIXME
            del ret.graph[ashery]
            del ret.graph[ammonia_plant]
            del ret.graph[clay_pit]

        if parameters["PRIMARY_INDUSTRY_GROWTH"] == "UNIVERSAL_SUPPLIES":
            if clay_pit in ret.graph:
                ret.graph[clay_pit].boosters = engineering_supplies
            ret.graph[peatlands].boosters = engineering_supplies
            ret.graph[phosphate_mine].boosters = engineering_supplies
            ret.graph[pyrite_mine].boosters = engineering_supplies

            ret.graph[fish_farm].boosters = engineering_supplies
            ret.graph[forest].boosters = engineering_supplies
            ret.graph[herding_coop].boosters = engineering_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies,)
                ret.graph[wharf].produces += (engineering_supplies,)
            else:
                ret.graph[paper_mill].produces += (engineering_supplies,)

        elif parameters["PRIMARY_INDUSTRY_GROWTH"] == "GENERIC_SUPPLIES":
            if clay_pit in ret.graph:
                ret.graph[clay_pit].boosters = engineering_supplies
            ret.graph[peatlands].boosters = engineering_supplies
            ret.graph[phosphate_mine].boosters = engineering_supplies
            ret.graph[pyrite_mine].boosters = engineering_supplies

            ret.graph[fish_farm].boosters = farm_supplies
            ret.graph[forest].boosters = farm_supplies
            ret.graph[herding_coop].boosters = farm_supplies

            if parameters["POLICY"] in ("SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"):
                ret.graph[port].produces += (engineering_supplies, farm_supplies)
                ret.graph[wharf].produces += (engineering_supplies, farm_supplies)
            else:
                ret.graph[paper_mill].produces += (engineering_supplies,)
                ret.graph[chemical_plant].produces += (farm_supplies,)

        self.default_worker_support(
            ret,
            (paper, zinc),
            (fishing_grounds,),
            (clay_pit, peatlands, phosphate_mine, pyrite_mine, fish_farm, forest, herding_coop),
            (ammonia_plant, ashery, chemical_plant, fishing_harbor, paper_mill, pyrite_smelter, sawmill),
        )

        if port in ret.graph:
            if parameters["SEA_INDUSTRY"] == "LAND_ONLY":
                ret.graph[trading_centre] = ret.graph[port]
                del ret.graph[port]
            elif parameters["SEA_INDUSTRY"] == "BOTH":
                ret.graph[trading_centre] = ret.graph[port]

        if parameters["TOWN_GOODS"] == "FOOD_AND_WATER":
            ret.graph[water_supply] = PrimaryIndustry(water)
            ret.graph[water_tower] = TertiaryIndustry(water)

        return ret
