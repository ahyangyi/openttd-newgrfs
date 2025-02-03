import functools
from agrf.magic import Switch
from agrf.lib.building.layout import ALayout


def lookup(thing, w, h, x, y, t):
    if isinstance(thing, (ALayout, int)):
        return thing
    return thing.lookup(w, h, x, y, t)


def calc_mode(d):
    value_count = {}
    for v in d.values():
        value_count[v] = value_count.get(v, 0) + 1
    max_count = max(value_count.values())
    return [v for v, c in value_count.items() if c == max_count][0]


class StationTileSwitch:
    def __init__(self, var, ranges, cb24=False):
        self.var = var
        self.ranges = {k: v for k, v in ranges.items() if v is not None}
        self.cb24 = cb24
        self.to_index_cache = {}

    @property
    def code(self):
        nibble = {"T": 24, "d": 12, "t": 8, "l": 4, "r": 0}[self.var]

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
    @functools.cache
    def T(self):
        return self.fmap(lambda x: x.T, special_property="T")

    @property
    @functools.cache
    def R(self):
        return self.fmap(lambda x: x.R, special_property="R")

    def to_index(self, sprite_list=None):
        if id(sprite_list) in self.to_index_cache:
            return self.to_index_cache[id(sprite_list)]
        mode = calc_mode(self.ranges)
        f = lambda v: v if isinstance(v, int) else v.to_index(sprite_list)
        new_ranges = {k: f(v) for k, v in self.ranges.items() if v != mode}
        if len(new_ranges) == 0:
            ret = f(mode)
        else:
            ret = Switch(ranges=new_ranges, default=f(mode), code=self.code)
        self.to_index_cache[id(sprite_list)] = ret
        return ret

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

    def demo(self, w, h, preswitch=None):
        return [
            [self.lookup(w, h, x, y, preswitch and preswitch.lookup(w, h, x, y)) for x in range(w)] for y in range(h)
        ]


def make_horizontal_switch(f):
    return StationTileSwitch("l", {l: StationTileSwitch("r", {r: f(l, r) for r in range(16)}) for l in range(16)})


def make_vertical_switch(f, cb24=False):
    return StationTileSwitch(
        "t", {t: StationTileSwitch("d", {d: f(t, d) for d in range(16)}, cb24) for t in range(16)}, cb24
    )
