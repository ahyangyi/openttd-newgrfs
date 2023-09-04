from industry.lib.economy import BaseEconomy
from industry.industries import gold_mine


class Economy(BaseEconomy):
    INDUSTRIES = [
        gold_mine,
    ]
    CARGOS = []
