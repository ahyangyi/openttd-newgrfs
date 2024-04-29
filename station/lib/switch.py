from agrf.magic import Switch


class StationTileSwitch:
    def __init__(self, var, ranges):
        code = StationTileSwitch.var2code[var]
        self.var = var
        self.ranges = ranges

    var2code = {
        "t": "var(0x41, shift=12, and=0x0000000f)",
        "d": "var(0x41, shift=8, and=0x0000000f)",
        "l": "var(0x41, shift=4, and=0x0000000f)",
        "r": "var(0x41, shift=0, and=0x0000000f)",
    }

    def fmap(self, f, special_property=None):
        new_var = (
            {"T": {"t": "d", "d": "t"}, "R": {"l": "r", "r": "l"}}.get(special_property, {}).get(self.var, self.var)
        )
        return StationTileSwitch(new_var, {k: f(v) for k, v in self.ranges.items()})

    @property
    def T(self):
        return self.fmap(lambda x: x.T, special_property="T")

    @property
    def R(self):
        return self.fmap(lambda x: x.R, special_property="R")

    def to_index(self, sprite_list):
        new_ranges = {k: v.to_index(sprite_list) for k, v in self.ranges.items()}
        return Switch(ranges=new_ranges, default=min(new_ranges.items())[1], code=self.var2code[self.var])

    def lookup(self, w, h, x, y):
        if self.var == "l":
            return self.ranges[min(x, 15)].lookup(w, h, x, y)
        elif self.var == "r":
            return self.ranges[min(w - x - 1, 15)].lookup(w, h, x, y)
        elif self.var == "t":
            return self.ranges[min(y, 15)].lookup(w, h, x, y)
        elif self.var == "d":
            return self.ranges[min(h - y - 1, 15)].lookup(w, h, x, y)
        else:
            raise NotImplementedError()


def make_horizontal_switch(f):
    return StationTileSwitch("l", {l: StationTileSwitch("r", {r: f(l, r) for r in range(16)}) for l in range(16)})
