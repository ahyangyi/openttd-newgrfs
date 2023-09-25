def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


class Economy:
    def __init__(self, name, graph, town_cargos):
        self.name = name
        self.graph = {
            x.the_industry: (tuple(x.the_cargo for x in make_tuple(i)), tuple(x.the_cargo for x in make_tuple(o)))
            for x, (i, o) in graph.items()
        }
        self.town_cargos = tuple(None if x is None else x.the_cargo for x in town_cargos)

    @property
    def industries(self):
        return list(self.graph.keys())

    @property
    def cargos(self):
        a = [i + o for i, o in self.graph.values()] + [x for x in self.town_cargos if x is not None]
        return list(
            set([x for i, o in self.graph.values() for x in i + o] + [x for x in self.town_cargos if x is not None])
        )
