from .reachability import check_reachability
from .climate_supplies import check_climate_supplies
from .yeti import check_yeti
from .id_uniqueness import check_id_uniqueness


def validate(economy):
    check_reachability(economy)
    check_climate_supplies(economy)
    check_yeti(economy)
    check_id_uniqueness(economy)
