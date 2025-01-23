import grf
import numpy as np

THIS_FILE = grf.PythonFile(__file__)


class EmptySprite(grf.Sprite):
    def __init__(self, w, h, zoom):
        self.w = w
        self.h = h
        self.zoom = zoom

    @property
    def bpp(self):
        return 8

    @property
    def default_name(self):
        return f"{self.w}x{self.h}"

    def prepare_files(self):
        pass

    def get_data_layers(self, context):
        return self.w, self.h, None, np.zeros(self.w, self.h, dtype=np.uint8)

    def get_image_files(self):
        return None

    def get_fingerprint(self):
        return grf.combine_fingerprint(w=self.w, h=self.h)

    def get_resource_files(self):
        return (THIS_FILE,)


def empty_alternatives(w, h):
    return grf.AlternativeSprites(EmptySprite(w, h, grf.ZOOM_OUT_8X))
