from .passes.reachability import check_reachability
from .passes.climate_supplies import check_climate_supplies
from .passes.yeti import check_yeti
from .passes.id_uniqueness import check_id_uniqueness
from .passes.trading import check_trading


def validate(economy):
    check_reachability(economy)
    check_climate_supplies(economy)
    check_yeti(economy)
    check_id_uniqueness(economy)
    check_trading(economy)
