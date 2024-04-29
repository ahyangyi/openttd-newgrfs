from agrf.magic import Switch
from .layout import ALayout


def lookup(thing, w, h, x, y, t):
    if isinstance(thing, (ALayout, int)):
        return thing
    return thing.lookup(w, h, x, y, t)


class StationTileSwitch:
    def __init__(self, var, ranges, cb24=False):
        self.var = var
        self.ranges = ranges
        self.cb24 = cb24

    @property
    def code(self):
        nibble = {"T": 24, "t": 12, "d": 8, "l": 4, "r": 0}[self.var]

        if self.cb24:
            return (f"(extra_callback_info1 >> {nibble}) & 0xf",)
        else:
            return (f"var(0x41, shift={nibble}, and=0x0000000f)",)

    def fmap(self, f, special_property=None):
        new_var = (
            {"T": {"t": "d", "d": "t"}, "R": {"l": "r", "r": "l"}}.get(special_property, {}).get(self.var, self.var)
        )
        return StationTileSwitch(new_var, {k: f(v) for k, v in self.ranges.items()}, cb24=self.cb24)

    @property
    def T(self):
        return self.fmap(lambda x: x.T, special_property="T")

    @property
    def R(self):
        return self.fmap(lambda x: x.R, special_property="R")

    def to_index(self, sprite_list):
        new_ranges = {k: v.to_index(sprite_list) for k, v in self.ranges.items()}
        return Switch(ranges=new_ranges, default=min(new_ranges.items())[1], code=self.code)

    def lookup(self, w, h, x, y, t=0):
        if self.var == "T":
            return lookup(self.ranges[t & 0x7], w, h, x, y, t)
        elif self.var == "l":
            return lookup(self.ranges[min(x, 15)], w, h, x, y, t)
        elif self.var == "r":
            return lookup(self.ranges[min(w - x - 1, 15)], w, h, x, y, t)
        elif self.var == "t":
            return lookup(self.ranges[min(y, 15)], w, h, x, y, t)
        elif self.var == "d":
            return lookup(self.ranges[min(h - y - 1, 15)], w, h, x, y, t)
        else:
            raise NotImplementedError()

    def demo(self, w, h):
        return [[self.lookup(w, h, x, y) for x in range(w)] for y in range(h)]


def make_horizontal_switch(f):
    return StationTileSwitch("l", {l: StationTileSwitch("r", {r: f(l, r) for r in range(16)}) for l in range(16)})


def make_vertical_switch(f):
    return StationTileSwitch("t", {t: StationTileSwitch("d", {d: f(t, d) for d in range(16)}) for t in range(16)})


def two_cb_demo(cb24, cb14):
    return [[cb14.lookup(w, h, x, y, cb24.lookup(w, h, x, y)) for x in range(w)] for y in range(h)]
