def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


class Economy:
    def __init__(self, name, graph, town_industries):
        self.name = name
        self.graph = {
            x.the_industry: (tuple(x.the_cargo for x in make_tuple(i)), tuple(x.the_cargo for x in make_tuple(o)))
            for x, (i, o) in graph.items()
        }
        self.town_industries = tuple(None if x is None else x.the_cargo for x in town_industries)

    @property
    def industries(self):
        return list(self.graph.keys())
