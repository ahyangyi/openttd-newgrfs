from .reachability import check_reachability
from .climate_supplies import check_climate_supplies


def validate(economy):
    check_reachability(economy)
    check_climate_supplies(economy)
