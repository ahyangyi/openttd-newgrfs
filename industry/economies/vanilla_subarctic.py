from industry.lib.economy import Economy
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


the_economy = Economy(
    name="Vanilla Sub-Arctic",
    industries=[
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
    ],
)
