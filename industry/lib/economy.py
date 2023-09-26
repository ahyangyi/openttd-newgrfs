def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


class PrimaryIndustryIO:
    def __init__(self, accepts=(), produces=()):
        self.accepts = accepts
        self.produces = produces

    @property
    def consumes(self):
        return ()


class SecondaryIndustryIO:
    def __init__(self, consumes=(), produces=()):
        self.consumes = consumes
        self.produces = produces

    @property
    def accepts(self):
        return self.consumes


class TownIO:
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
    def __init__(self, name, graph, town_cargos):
        self.name = name
        self.graph = {
            x.the_industry: (make_tuple(i), make_tuple(o))
            for x, (i, o) in graph.items()
        }
        self.town_cargos = town_cargos

    @property
    def industries(self):
        return list(self.graph.keys())

    @property
    def cargos(self):
        a = [i + o for i, o in self.graph.values()] + [x for x in self.town_cargos if x is not None]
        return list(
            set([x for i, o in self.graph.values() for x in i + o] + [x for x in self.town_cargos if x is not None])
        )
