from agrf.graphics import LayeredImage


class Demo:
    def __init__(self, title, tiles, remap=None):
        self.title = title
        self.tiles = tiles
        self.remap = remap

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
                subimg = sprite.graphics(remap, scale, bpp)
                img.blend_over(subimg.move((32 * r - 32 * c) * scale, (16 * r + 16 * c) * scale))
        return img

    @property
    def M(self):
        return Demo(
            self.title, [[tile and tile.M for tile in row[::-1]] for row in list(zip(*self.tiles))[::-1]], self.remap
        )
