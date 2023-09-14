def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


class Economy:
    def __init__(self, name, graph):
        self.name = name
        self.graph = {
            x.the_industry: (tuple(x.the_cargo for x in make_tuple(i)), tuple(x.the_cargo for x in make_tuple(o)))
            for x, (i, o) in graph.items()
        }
        self.industries = list(self.graph.keys())
