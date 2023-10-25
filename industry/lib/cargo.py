import grf
import struct
from agrf.lib.cargo import Cargo
from cargos import cargos as cargo_table
from agrf.strings import get_translation


class ACargo(Cargo):
    def __init__(self, id, label, cargo_class, capacity_multiplier=0x100, weight=16, **props):
        super().__init__(
            id,
            **{
                "classes": cargo_class,
                "capacity_mult": capacity_multiplier,
                "weight": weight,
                **props,
            },
        )
        self.label = label
        self.cargo_class = cargo_class

    def get_sprites(self, g):
        s = g.strings
        self._props["type_text"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["unit_text"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["one_text"] = s[f"STR_CARGO_UNIT_{self.label.decode()}"]
        self._props["many_text"] = s[f"STR_CARGO_UNIT_{self.label.decode()}"]
        self._props["abbr_text"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["bit_number"] = self.id
        self._props["label"] = struct.unpack("<I", self.label)[0]
        return super().get_sprites(g)

    @property
    def capacity_multiplier(self):
        return self._props["capacity_mult"]

    @property
    def weight(self):
        return self._props["weight"]

    @property
    def translated_id(self):
        return cargo_table.index(self.label)

    def __repr__(self):
        return f"<Cargo:{self.label}>"

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_CARGO_NAME_{self.label.decode()}"], 0x7F)
