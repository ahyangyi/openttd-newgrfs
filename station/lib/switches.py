from agrf.magic.switch import Switch


class StationTileSwitch(Switch):
    var2code = {
            "t": "var(0x41, shift=12, and=0x0000000f)"
            "d": "var(0x41, shift=8, and=0x0000000f)"
            "l": "var(0x41, shift=4, and=0x0000000f)"
            "r": "var(0x41, shift=0, and=0x0000000f)"
        }

    def lookup(self, w, h, x, y):

def make_horizontal_switch(cb):
