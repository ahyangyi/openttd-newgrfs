def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


class PrimaryIndustry:
    def __init__(self, produces=(), accepts=()):
        self.produces = make_tuple(produces)
        self.accepts = make_tuple(accepts)

    @property
    def consumes(self):
        return ()


class SecondaryIndustry:
    def __init__(self, consumes=(), produces=()):
        self.consumes = make_tuple(consumes)
        self.produces = make_tuple(produces)

    @property
    def accepts(self):
        return self.consumes


class TertiaryIndustry:
    def __init__(self, consumes=()):
        self.consumes = make_tuple(consumes)

    @property
    def accepts(self):
        return self.consumes

    @property
    def produces(self):
        return ()


class Town:
    def __init__(self, passengers, mail, food, goods):
        self.passengers = passengers
        self.mail = mail
        self.food = food
        self.goods = goods

    @property
    def accepts(self):
        make_tuple = lambda x: () if x is None else (x,)
        return tuple(y for x in (self.passengers, self.mail, self.food, self.goods) for y in make_tuple(x))

    @property
    def consumes(self):
        return ()

    @property
    def produces(self):
        make_tuple = lambda x: () if x is None else (x,)
        return tuple(y for x in (self.passengers, self.mail) for y in make_tuple(x))


class Economy:
    def __init__(self, name, graph):
        self.name = name
        self.graph = graph

    @property
    def industries(self):
        return list(self.graph.keys())

    @property
    def cargos(self):
        return list(set(y for x in self.graph.values() for y in x.accepts + x.produces))
