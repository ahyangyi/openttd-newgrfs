import grf
import struct
from industry.lib.parameters import parameter_list
from agrf.lib.cargo import Cargo
from cargos import cargos as cargo_table, voxel_map
from agrf.strings import get_translation
from agrf.split_action import MetaSpriteMixin
from agrf.graphics.voxel import LazyVoxel


class CargoUnit:
    PASSENGER = 0x4F
    TONNE = 0x50
    BAG = 0x51
    LITRE = 0x52
    ITEM = 0x53
    CRATE = 0x54


# FIXME: merge with the other props_hash
def props_hash(parameters):
    ret = []
    for k, v in sorted(parameters.items()):
        ret.append((k, v))
    return hash(tuple(ret))


class ACargo(Cargo, MetaSpriteMixin):
    def __init__(self, id, label, cargo_class, capacity_multiplier=0x100, weight=16, **props):
        graphics = None
        if label.decode() in voxel_map:
            voxel_name = voxel_map[label.decode()]
            vox = LazyVoxel(
                voxel_name,
                prefix=".cache/render/cargo/",
                voxel_getter=lambda: f"cargos/voxels/{voxel_name}.vox",
                load_from="cargos/files/gorender.json",
            )
            vox.config["size"]["x"] = 152
            vox.config["size"]["y"] = 152
            graphics = vox.spritesheet()[0]

        super().__init__(
            id=id,
            **{"cargo_classes": cargo_class, "capacity_multiplier": capacity_multiplier, "weight": weight, **props},
            graphics=graphics,
        )
        MetaSpriteMixin.__init__(self, grf.CARGO, props_hash, parameter_list)
        self.label = label
        self.cargo_class = cargo_class

    def postprocess_props(self, props):
        return ACargo.translate_strings(props, self._g)

    def get_definitions(self, g):
        res = self.dynamic_definitions()
        return [sprite for sprite_group in res for sprite in sprite_group]

    def get_sprites(self, g):
        s = g.strings
        self._props["type_name"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["unit_name"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["one_text"] = s[f"STR_CARGO_UNIT_{self.label.decode()}"]
        self._props["many_text"] = s[f"STR_CARGO_UNIT_{self.label.decode()}"]
        self._props["type_abbreviation"] = s[f"STR_CARGO_NAME_{self.label.decode()}"]
        self._props["bit_number"] = self.id
        self._props["label"] = struct.unpack("<I", self.label)[0]
        self._g = g  # FIXME?

        return super().get_sprites(g)

    @property
    def capacity_multiplier(self):
        return self._props["capacity_multiplier"]

    @property
    def weight(self):
        return self._props["weight"]

    @property
    def translated_id(self):
        return cargo_table.index(self.label)

    def __repr__(self):
        return f"<Cargo:{self.label}>"

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_CARGO_NAME_{self.label.decode()}"], lang_id)

    @property
    def penalty1(self):
        return self._props["penalty_lowerbound"]

    @property
    def penalty2(self):
        return self._props["single_penalty_length"]

    @property
    def base_price(self):
        return self._props["base_price"]
