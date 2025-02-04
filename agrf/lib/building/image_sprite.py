import grf
from agrf.graphics import SCALE_TO_ZOOM


def image_sprite(path, crop=True):
    return grf.AlternativeSprites(
        grf.FileSprite(grf.ImageFile(path), 0, 0, 256, 127, xofs=-124, yofs=0, bpp=32, zoom=SCALE_TO_ZOOM[4], crop=crop)
    )
