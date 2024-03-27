from road_vehicle.lib.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from agrf.graphics import LayeredImage
import grf

ALLOWED_FLAGS = ["noflipX", "noflipY", "debug_bbox"]


class AutoWolf:
    def __init__(
        self, name, lengths=(1, 1, 4, 1, 1), segments=(None, None, (0, 8), None, None), rotation_steps=1, flags=tuple()
    ):
        if type(name) is not list and type(name) is not tuple:
            name = [name]
        self.lengths = lengths
        self.segments = segments
        self.hill_variants = [(-2, -11.536959), (-1, -5.7684795), (0, 0), (1, 5.7684795), (2, 11.536959)]
        self.rotation_steps = rotation_steps
        assert all(f in ALLOWED_FLAGS for f in flags), flags
        self.flags = flags

        vanilla_graphics = {}
        name_i = 0
        self.xdiff = {}
        for i, seg in enumerate(segments):
            if seg is not None:
                self.xdiff[i] = (8 - seg[0] - seg[1]) / 2 + sum(lengths[:i])
                if isinstance(name[name_i], str):
                    vanilla_graphics[i] = LazyVoxel(name[name_i])
                else:
                    vanilla_graphics[i] = name[name_i]

                # XXX Shadow-rotate negates xdiff as well
                if isinstance(vanilla_graphics[i], tuple):
                    self.xdiff[i] = -self.xdiff[i]

                name_i += 1

        self.graphics = {}
        self.shifts = {}
        for i, switch in vanilla_graphics.items():
            # FIXME
            if isinstance(switch, tuple):
                switch, shadow_rotate = switch[0], True
            else:
                switch, shadow_rotate = switch, False

            if "debug_bbox" in flags:
                self.graphics[i] = switch
                self.shifts[i] = 0
                continue

            # Make hill switches
            hill_voxels = [switch.change_pitch(pitch, f"hill{hil}") for hil, pitch in self.hill_variants]
            ranges = {(-127, -3): 0, (-2, -1): 1, (1, 2): 3, (3, 127): 4}
            if shadow_rotate:
                assert all(a == -c and b == -d for (a, b), (c, d) in zip(self.hill_variants, self.hill_variants[::-1]))
                ranges = {k: len(self.hill_variants) - 1 - v for k, v in ranges.items()}

            front_z_2 = "(var(0x62, param=0xfe, shift=0, and=0xff000000) >> 24)"
            front_z = "(var(0x62, param=0xff, shift=0, and=0xff000000) >> 24)"
            back_z = "(var(0x62, param=0x01, shift=0, and=0xff000000) >> 24)"
            back_z_2 = "(var(0x62, param=0x02, shift=0, and=0xff000000) >> 24)"

            switch = Switch(
                ranges={k: hill_voxels[v] for k, v in ranges.items()},
                default=hill_voxels[2],
                code=f"{front_z_2} + {front_z} + {back_z} + {back_z_2}",
            )

            # Make rotate switches
            rot_voxels = [
                switch.rotate(rot * 45 / (rotation_steps * 2 + 1), f"rot{rot}")
                for rot in range(-rotation_steps, rotation_steps + 1)
            ]

            front_d = "(var(0x62, param=0xff, shift=0, and=0x0000000f))"
            back_d = "(var(0x62, param=0x01, shift=0, and=0x0000000f))"

            switch = Switch(
                ranges={(4, 7): rot_voxels[0], (1, 3): rot_voxels[2]},
                default=rot_voxels[1],
                code=f"({front_d} - {back_d}) & 0x7",
            )

            # Make night switches
            night_voxels = switch.update_config({"lighting_weight": 0.3}, "night")
            switch = Switch(
                ranges={1: night_voxels, (4, 5): night_voxels},
                default=switch,
                code="(var(0x7F, param=0x1, shift=1, and=0x00000006)) + (var(0x7F, param=0x41, shift=0, and=0x00000001))",
            )

            # Make flipped switches
            flipped_voxels = switch.flip("flip")
            if "noflipY" not in self.flags:
                switch = Switch(ranges={0: switch}, default=flipped_voxels, code="traffic_side")
            else:
                switch = flipped_voxels

            self.graphics[i] = switch
            self.shifts[i] = 4 if shadow_rotate else 0

    def doc_graphics(self, remap):
        img = LayeredImage.empty()
        for k, v in self.graphics.items():
            v = v.get_default_graphics()
            sprite = v.spritesheet()
            sprite = sprite[3 + self.shifts[k]]
            masked_sprite = LayeredImage.from_sprite(sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)).copy()
            masked_sprite.remap(remap)
            masked_sprite.apply_mask()
            diff = sum(self.lengths[:k])
            img.blend_over(masked_sprite.move(8 * diff, 4 * diff))
        return img.crop().to_pil_image()

    def empty(self):
        return grf.GenericSpriteLayout(ent1=(31,), ent2=(31,))

    def callbacks(self, my_id, cargo_capacity, feature):
        seg_map = {}
        for i, seg in enumerate(self.segments):
            if seg is not None:
                seg_map[i] = len(seg_map)

        return {
            "articulated_part": grf.DualCallback(
                default=grf.Switch(
                    ranges={i: my_id for i in range(1, len(self.segments))},
                    default=0x7FFF,
                    code="extra_callback_info1_byte",
                ),
                purchase=0x7FFF,
            ),
            "properties": {
                "shorten_by": grf.Switch(
                    ranges={i: 8 - l for i, l in enumerate(self.lengths)}, default=0, code="position_in_articulated_veh"
                ),
                "cargo_capacity": grf.DualCallback(
                    default=grf.Switch(
                        ranges={i: cargo_capacity for i, r in enumerate(self.segments) if r is not None},
                        default=0,
                        code="position_in_articulated_veh",
                    ),
                    purchase=cargo_capacity,
                ),
            },
            "graphics": grf.Switch(
                ranges={
                    i: grf.Switch(
                        ranges={0: self.graphics[i].get_action(feature, self.xdiff[i], self.shifts[i])},
                        default=self.graphics[i]
                        .get_default_graphics()
                        .get_action(feature, self.xdiff[i], self.shifts[i]),
                        code="extra_callback_info1_byte",
                    )
                    for i, seg in enumerate(self.segments)
                    if seg is not None
                },
                default=self.empty(),
                code="position_in_articulated_veh",
            ),
        }
