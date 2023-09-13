class Economy:
    def __init__(self, name, graph):
        self.name = name
        self.graph = {
            x.the_industry: (tuple(x.the_cargo for x in i), tuple(x.the_cargo for x in o))
            for x, (i, o) in graph.items()
        }
        self.industries = list(self.graph.keys())
