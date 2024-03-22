import grf
from PIL import Image


class AStation(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, sprites, layouts, callbacks=None, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.sprites = sprites
        self.layouts = layouts
        if callbacks is None:
            callbacks = {}
        self.callbacks = grf.make_callback_manager(grf.STATION, callbacks)
        self._props = props

    def get_sprites(self, g):
        res = []

        name = g.strings[f"STR_STATION_{self.translation_name}_NAME"]
        class_name = g.strings[f"STR_STATION_CLASS_{self._props['class_label'].decode()}"]

        if self.sprites:
            layouts = []
            for i in range(len(self.sprites)):
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


class BinaryVariantWrapper:
    def __init__(self, obj):
        self.obj = obj
        self.variants = None

    @staticmethod
    def create_variants(factory, variants):
        ret = [factory(v) for v in variants]
        for i, r in enumerate(ret):
            r.variants = [ret[i ^ j] for j in range(len(ret))]
        return ret[0]

    def __getattr__(self, name):
        def method(*args, **kwargs):
            call = lambda x: getattr(x, name)(*args, **kwargs)
            return getattr(self.obj, name)(*args, **kwargs)

        return method

    def __repr__(self):
        return f"<BinaryVariant:{repr(self.obj)}>"

    @property
    def all_variants(self):
        return self.variants

    def __getitem__(self, index):
        return self.variants[index]

    def to_index(self, sprite_pool):
        return sprite_pool.index(self)


class BuildingSpriteSheetFull(BinaryVariantWrapper):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantWrapper.create_variants(BuildingSpriteSheetFull, sprites)

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


class BuildingSpriteSheetSymmetricalX(BinaryVariantWrapper):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantWrapper.create_variants(BuildingSpriteSheetSymmetricalX, [sprites[i] for i in [0, 1, 4, 5]])

    @property
    def C(self):
        return self

    @property
    def T(self):
        return self[2]


class BuildingSpriteSheetSymmetricalY(BinaryVariantWrapper):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantWrapper.create_variants(BuildingSpriteSheetSymmetricalY, [sprites[i] for i in [0, 1, 2, 3]])

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]

    @property
    def T(self):
        return self


class BuildingSpriteSheetSymmetrical(BinaryVariantWrapper):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantWrapper.create_variants(BuildingSpriteSheetSymmetricalY, [sprites[i] for i in [0, 1]])

    @property
    def T(self):
        return self


groundsprite = Image.open("third_party/opengfx2/1012.png")


class Demo:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles

    def doc_graphics(self, remap):
        from agrf.graphics.attach_over import attach_over
        from agrf.graphics.blend import blend

        img = Image.new(
            "RGBA", (128 * (len(self.tiles) + len(self.tiles[0])), 200 + 64 * (len(self.tiles) + len(self.tiles[0])))
        )
        for r, row in enumerate(self.tiles):
            for c, sprite in enumerate(row[::-1]):
                if sprite is None:
                    continue
                masked_sprite = sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)
                subimg, _ = masked_sprite.sprite.get_image()
                submask, _ = masked_sprite.mask.get_image()
                submask = remap.remap_image(submask)
                subimg = blend(subimg, submask)
                # FIXME: doesn't align
                # img = attach_over(groundsprite, img, (-128 * (len(row) - 1) - 128 * r + 128 * c, -341 - 64 * r - 64 * c))
                img = attach_over(subimg, img, (-128 * (len(row) - 1) - 128 * r + 128 * c, -200 - 64 * r - 64 * c))
        return img.crop(img.getbbox())


class AMetaStation:
    def __init__(self, stations, class_label, doc_sprites, doc_layouts):
        self.stations = stations
        self.class_label = class_label
        self.doc_sprites = doc_sprites
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
