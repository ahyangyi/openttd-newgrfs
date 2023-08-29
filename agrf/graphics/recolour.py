class ColourRange:
    def __init__(self, a, b=None):
        if b is None:
            b = a
        self.a = a
        self.b = b

    def __str__(self):
        return f"{self.a}-{self.b}"


class ColourMap:
    def __init__(self, name, colour_map):
        self.name = name
        self.colour_map = colour_map

    def positor_config(self):
        return {
            "input_ramps": [str(x) for x, _ in self.colour_map],
            "output_ramps": [str(x) for _, x in self.colour_map],
        }
