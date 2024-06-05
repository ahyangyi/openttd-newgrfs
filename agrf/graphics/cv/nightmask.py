import numpy as np
from .. import LayeredImage


def make_night_mask(img: LayeredImage, darkness=0.75) -> LayeredImage:
    assert img.alpha is not None

    return LayeredImage(
        xofs=img.xofs,
        yofs=img.yofs,
        w=img.w,
        h=img.h,
        rgb=np.zeros((img.h, img.w, 3), dtype=np.uint8),
        alpha=(img.alpha * darkess).astype(np.uint8),
        mask=None,
    )
