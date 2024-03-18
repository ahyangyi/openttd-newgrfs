import grf


class AStation(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, sprites, layouts, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.sprites = sprites
        self.layouts = layouts
        self.callbacks = grf.make_callback_manager(grf.STATION, callbacks)
        self._props = props

    def get_sprites(self, g):
        res = []

        name = g.strings[f"STR_STATION_{self.translation_name}_NAME"]
        class_name = g.strings[f"STR_STATION_CLASS_{self._props['class_label'].decode()}"]

        if self.sprites:
            layouts = []
            for i, sprite in enumerate(self.sprites):
                layouts.append(grf.GenericSpriteLayout(ent1=[i], ent2=[i], feature=grf.STATION))
            self.callbacks.graphics = layouts[0]

        self.callbacks.set_flag_props(self._props)

        res.append(
            definition := grf.Define(
                feature=grf.STATION,
                id=self.id,
                props={
                    "class_label": self._props["class_label"],
                    "advanced_layout": grf.SpriteLayoutList(self.layouts),
                    **self._props,
                },
            )
        )
        if self.sprites:
            res.append(grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(self.sprites)))

            for s in self.sprites:
                res.append(s)

        res.extend(self.callbacks.make_map_action(definition))
        res.extend(class_name.get_actions(grf.STATION, 0xC400 + self.id, is_generic_offset=True))
        res.extend(name.get_actions(grf.STATION, 0xC500 + self.id, is_generic_offset=True))

        return res


class BuildingSpriteSheet:
    def __init__(self, things):
        self.things = things

    def all(self):
        return self.things

    def __getitem__(self, index):
        return type(self)([self.things[index ^ x] for x in range(len(self.things))])

    @property
    def sprite(self):
        return self.things[0]


class BuildingSpriteSheetFull(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetFull(things)

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]

    @property
    def T(self):
        return self[4]

    @property
    def TL(self):
        return self[4]

    @property
    def TR(self):
        return self[6]


class BuildingSpriteSheetSymmetricalX(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetricalX([things[0], things[1], things[4], things[5]])

    @property
    def C(self):
        return self

    @property
    def T(self):
        return self[2]


class BuildingSpriteSheetSymmetricalY(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetricalY([things[0], things[1], things[2], things[3]])

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]

    @property
    def T(self):
        return self


class BuildingSpriteSheetSymmetrical(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetrical([things[0], things[1]])

    @property
    def T(self):
        return self


class Demo:
    def __init__(self, tiles):
        self.tiles = tiles

    def doc_graphics(self, remap):
        from agrf.graphics.attach_over import attach_over
        from agrf.graphics.blend import blend
        from PIL import Image

        img = Image.new("RGBA", (2000, 2000))
        for r, row in enumerate(self.tiles):
            for c, sprite in enumerate(row[::-1]):
                if sprite is None:
                    continue
                masked_sprite = sprite.sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)
                subimg, _ = masked_sprite.sprite.get_image()
                submask, _ = masked_sprite.mask.get_image()
                submask = remap.remap_image(submask)
                subimg = blend(subimg, submask)
                img = attach_over(subimg, img, (-128 * (len(row) - 1) - 128 * r + 128 * c, -200 - 64 * r - 64 * c))
        return img.crop(img.getbbox())


def fixup_callback(thing, sprites):
    if isinstance(thing, grf.Switch):
        return grf.Switch(
            ranges={(r.low, r.high): fixup_callback(r.ref, sprites) for r in thing._ranges},
            default=fixup_callback(thing.default, sprites),
            code=thing.code,
        )
    if isinstance(thing, BuildingSpriteSheet):
        return sprites.index(thing.sprite)
    return thing


class AMetaStation:
    def __init__(self, stations, class_label, doc_layouts):
        self.stations = stations
        self.class_label = class_label
        self.doc_layouts = doc_layouts

    def add(self, g):
        for station in self.stations:
            g.add(station)


def simple_layout(ground_sprite, sprite_id):
    return grf.SpriteLayout(
        [
            grf.GroundSprite(
                sprite=grf.SpriteRef(
                    id=ground_sprite,
                    pal=0,
                    is_global=True,
                    use_recolour=False,
                    always_transparent=False,
                    no_transparent=False,
                ),
                flags=0,
            ),
            grf.ParentSprite(
                sprite=grf.SpriteRef(
                    id=0x42D + sprite_id,
                    pal=0,
                    is_global=False,
                    use_recolour=True,
                    always_transparent=False,
                    no_transparent=False,
                ),
                extent=(16, 16, 48),
                offset=(0, 0, 0),
                flags=0,
            ),
        ]
    )
