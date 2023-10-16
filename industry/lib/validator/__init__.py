from .reachability import check_reachability
from .climate_supplies import check_climate_supplies
from .yeti import check_yeti


def validate(economy):
    check_reachability(economy)
    check_climate_supplies(economy)
    check_yeti(economy)
