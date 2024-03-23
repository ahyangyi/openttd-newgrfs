import grf
from PIL import Image
from agrf.graphics.attach_over import attach_over
from agrf.graphics.blend import blend


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


class BinaryVariantMixin:
    @staticmethod
    def create_variants(classobj, variants):
        for i, v in enumerate(variants):
            cls = v.__class__
            v.__class__ = type(cls.__name__, (classobj, cls), {})
            v.variants = [variants[i ^ j] for j in range(len(variants))]
        return variants[0]

    def __repr__(self):
        return f"<BinaryVariant:{repr(super())}>"

    @property
    def all_variants(self):
        return self.variants

    def __getitem__(self, index):
        return self.variants[index]

    def to_index(self, sprite_pool):
        return sprite_pool.index(self)

    @property
    def M(self):
        return self[1]


class BuildingSpriteSheetFull(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantMixin.create_variants(BuildingSpriteSheetFull, sprites)

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


class BuildingSpriteSheetSymmetricalX(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantMixin.create_variants(BuildingSpriteSheetSymmetricalX, [sprites[i] for i in [0, 1, 4, 5]])

    @property
    def C(self):
        return self

    @property
    def T(self):
        return self[2]


class BuildingSpriteSheetSymmetricalY(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantMixin.create_variants(BuildingSpriteSheetSymmetricalY, [sprites[i] for i in [0, 1, 2, 3]])

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]

    @property
    def T(self):
        return self


class BuildingSpriteSheetSymmetrical(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def from_complete_list(sprites):
        return BinaryVariantMixin.create_variants(BuildingSpriteSheetSymmetricalY, [sprites[i] for i in [0, 1]])

    @property
    def T(self):
        return self


groundsprite = Image.open("third_party/opengfx2/1012.png")


class Demo:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles

    def doc_graphics(self, remap):
        img = Image.new(
            "RGBA", (128 * (len(self.tiles) + len(self.tiles[0])), 200 + 64 * (len(self.tiles) + len(self.tiles[0])))
        )
        for r, row in enumerate(self.tiles):
            for c, sprite in enumerate(row[::-1]):
                if sprite is None:
                    continue
                subimg = sprite.doc_graphics(remap)
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


class ADefaultGroundSprite:
    def __init__(self, sprite):
        self.sprite = sprite

    def to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=self.sprite,
                pal=0,
                is_global=True,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        )

    @property
    def L(self):
        return self

    R = T = TL = TR = L

    @property
    def M(self):
        return ADefaultGroundSprite(self.sprite - 1 if self.sprite % 2 == 0 else self.sprite + 1)


class AGroundSprite:
    def __init__(self, sprite):
        self.sprite = sprite

    def to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        )

    # FIXME add methods


class AParentSprite:
    def __init__(self, sprite, extent, offset):
        self.sprite = sprite
        self.extent = extent
        self.offset = offset

    def to_grf(self, sprite_list):
        return grf.ParentSprite(
            sprite=grf.SpriteRef(
                id=0x42D + sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=True,
                always_transparent=False,
                no_transparent=False,
            ),
            extent=self.extent,
            offset=self.offset,
            flags=0,
        )

    @property
    def L(self):
        return self

    @property
    def M(self):
        mirror = lambda x: (x[1], x[0], x[2])
        return AParentSprite(self.sprite.M, mirror(self.extent), mirror(self.offset))

    @property
    def R(self):
        new_offset = (16 - self.offset[0] - self.extent[0], self.offset[1], self.offset[2])
        return AParentSprite(self.sprite.R, self.extent, new_offset)

    @property
    def T(self):
        new_offset = (self.offset[0], 16 - self.offset[1] - self.extent[1], self.offset[2])
        return AParentSprite(self.sprite.T, self.extent, new_offset)

    TL = T

    @property
    def TR(self):
        return self.T.R


class ALayout:
    def __init__(self, ground_sprite, sprites):
        self.ground_sprite = ground_sprite
        self.sprites = sprites

    def to_grf(self, sprite_list):
        return grf.SpriteLayout(
            [self.ground_sprite.to_grf(sprite_list)] + [sprite.to_grf(sprite_list) for sprite in self.sprites]
        )

    def __getattr__(self, name):
        call = lambda x: getattr(x, name)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = [call(sprite) for sprite in self.sprites]
        return ALayout(new_ground_sprite, new_sprites)

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = call(self.sprites)
        return ALayout(new_ground_sprite, new_sprites)

    def doc_graphics(self, remap):
        img = None
        for sprite in self.sprites:
            masked_sprite = sprite.sprite.get_sprite(zoom=grf.ZOOM_4X, bpp=32)
            subimg, _ = masked_sprite.sprite.get_image()
            submask, _ = masked_sprite.mask.get_image()
            submask = remap.remap_image(submask)
            subimg = blend(subimg, submask)
            # img = attach_over(subimg, img, (-128 * (len(row) - 1) - 128 * r + 128 * c, -200 - 64 * r - 64 * c))
            img = subimg
        return img


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
