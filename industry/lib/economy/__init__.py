import functools
from agrf.strings import get_translation
from industry.cargos import engineering_supplies, farm_supplies, tired_workers, workers
from .industry_desc import PrimaryIndustry, WorkerYard, FreePort, SecondaryIndustry, TertiaryIndustry, Town
from .worker_mixin import WorkerMixin


class Economy:
    def __init__(self, graph, parameters):
        self.graph = graph
        self.parameters = parameters

    @property
    @functools.cache
    def industries(self):
        return list(self.graph.keys())

    @property
    @functools.cache
    def cargos(self):
        return list(set(y for x in self.graph.values() for y in x.accepts + x.produces))

    @property
    def parameter_desc(self):
        from industry.lib.parameters import parameter_choices

        return parameter_choices.desc(self.parameters)

    @property
    def collapsed_cargos(self):
        return [x for x in [engineering_supplies, farm_supplies, workers, tired_workers] if x in self.cargos]


class MetaEconomy(WorkerMixin):
    def __init__(self, translation_name):
        self.translation_name = translation_name

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_PARAM_ECONOMY_{self.translation_name}"], 0x7F)
