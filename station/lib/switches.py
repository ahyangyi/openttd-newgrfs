from agrf.magic.switch import Switch


class StationTileSwitch(Switch):
    def __init__(self, var, ranges, default):
        code = StationTileSwitch.var2code[var]
        super().__init__(code, ranges, default)
        self.var = var

    var2code = {
            "t": "var(0x41, shift=12, and=0x0000000f)"
            "d": "var(0x41, shift=8, and=0x0000000f)"
            "l": "var(0x41, shift=4, and=0x0000000f)"
            "r": "var(0x41, shift=0, and=0x0000000f)"
        }

    def derive(self, callback):
        return StationTileSwitch(
            self.var,
            {(r.low, r.high): callback(r.ref) for r in self._ranges},
            callback(self.default),
        )

    def lookup(self, w, h, x, y):
        if self.var == "l":
            pass
        else:
            raise NotImplementedError()

def make_horizontal_switch(cb):
