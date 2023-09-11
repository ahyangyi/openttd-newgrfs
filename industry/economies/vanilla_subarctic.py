from industry.lib.economy import BaseEconomy
from industry.industries import (
    bank,
    coal_mine,
    food_processing_plant,
    farm,
    forest,
    paper_mill,
    oil_refinery,
    printing_works,
    oil_wells,
    power_station,
    gold_mine,
)


class Economy(BaseEconomy):
    INDUSTRIES = [
        bank,
        coal_mine,
        food_processing_plant,
        farm,
        forest,
        paper_mill,
        oil_refinery,
        printing_works,
        oil_wells,
        power_station,
        gold_mine,
    ]
    CARGOS = []
