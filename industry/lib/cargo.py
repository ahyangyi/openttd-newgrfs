import grf
import struct


class ACargo(grf.SpriteGenerator):
    def __init__(self, label, cargo_class, capacity_multiplier=0x100, weight=16, **props):
        self.label = label
        self.cargo_class = cargo_class
        self.capacity_multiplier = capacity_multiplier
        self.weight = weight
        self._props = {
            "label": struct.unpack("<I", label)[0],
            "classes": cargo_class,
            "capacity_mult": capacity_multiplier,
            "weight": weight,
            **props,
        }
        self.callbacks = grf.make_callback_manager(grf.CARGO, {})

    def get_sprites(self, g):
        res = []
        res.append(definition := grf.Define(feature=grf.CARGO, id=0, props=self._props))
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res

    def __repr__(self):
        return f"<Cargo:{self.label}>"
