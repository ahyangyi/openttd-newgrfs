from agrf.graphics import LayeredImage
from agrf.utils import unique_tuple


class Demo:
    def __init__(self, title, tiles, remap=None, climate="temperate", subclimate="default"):
        self.title = title
        self.tiles = tiles
        self.remap = remap
        self.climate = climate
        self.subclimate = subclimate

    def graphics(self, scale, bpp, remap=None):
        remap = remap or self.remap
        yofs = 32 * scale
        img = LayeredImage.canvas(
            -16 * scale * (len(self.tiles) + len(self.tiles[0])),
            -yofs,
            32 * scale * (len(self.tiles) + len(self.tiles[0])),
            yofs + 16 * scale * (len(self.tiles) + len(self.tiles[0])),
            has_mask=remap is None,
        )

        for r, row in enumerate(self.tiles):
            for c, sprite in enumerate(row[::-1]):
                if sprite is None:
                    continue
                subimg = sprite.graphics(scale, bpp, remap=remap, climate=self.climate, subclimate=self.subclimate)
                img.blend_over(subimg.move((32 * r - 32 * c) * scale, (16 * r + 16 * c) * scale))
        return img

    @property
    def T(self):
        return Demo(self.title, [[tile and tile.T for tile in row] for row in self.tiles[::-1]], self.remap)

    @property
    def M(self):
        return Demo(
            self.title, [[tile and tile.M for tile in row[::-1]] for row in list(zip(*self.tiles))[::-1]], self.remap
        )

    def get_fingerprint(self):
        return {"tiles": [[x and x.get_fingerprint() for x in row] for row in self.tiles], "remap": "FIXME"}  # FIXME

    def get_resource_files(self):
        return unique_tuple(f for row in self.tiles for x in row for f in x.get_resource_files())
