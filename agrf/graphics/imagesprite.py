import grf


class ImageSprite(grf.ImageSprite):
    def __init__(self, image, fingerprint, **kw):
        super().__init__(image, **kw)
        self.fingerprint = fingerprint

    def get_fingerprint(self):
        return self.fingerprint
