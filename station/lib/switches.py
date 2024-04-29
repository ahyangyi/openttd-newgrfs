from agrf.magic import CachedFunctorMixin


class StationTileSwitch(CachedFunctorMixin):
    def __init__(self, var, ranges):
        super().__init__()
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
        return StationTileSwitch(new_var, {k: f(v) for k, v in self.ranges})

    def lookup(self, w, h, x, y):
        if self.var == "l":
            pass
        else:
            raise NotImplementedError()


def make_horizontal_switch(f):
    return StationTileSwitch("l", {StationTileSwitch("r", {f(l, r) for r in range(16)}) for l in range(16)})
