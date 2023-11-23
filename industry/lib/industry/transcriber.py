import grf


class OldIndustryTileID:
    def __init__(self, id):
        self.id = id

    def __call__(self, xofs, yofs):
        return grf.IndustryLayout.OldTile(
            xofs=xofs,
            yofs=yofs,
            id=0,
        )


class NewIndustryTileID:
    def __init__(self, id):
        self.id = id

    def __call__(self, xofs, yofs):
        return grf.IndustryLayout.NewTile(
            xofs=xofs,
            yofs=yofs,
            id=0,
        )


def transcribe_one(pattern, registry):
    ret = []
    for i, r in enumerate(pattern):
        for j, c in enumerate(r):
            if c != " ":
                ret.append(registry[c](i, j))
    return grf.IndustryLayout(ret)


def transcribe(patterns, registry):
    return [transcribe_one(p, registry) for p in patterns]
