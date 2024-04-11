import grf
from .utils import class_label_printable


class AMetaStation(grf.SpriteGenerator):
    def __init__(self, stations, class_label, categories, doc_layouts, demos):
        super().__init__()
        self.stations = stations
        self.class_label = class_label
        self.categories = categories
        self.doc_layouts = doc_layouts
        self.demos = demos

    @property
    def class_label_plain(self):
        return class_label_printable(self.class_label)

    def get_sprites(self, g):
        sprites = self.sprites
        return (
            [grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(sprites))]
            + self.sprites
            + [s for station in self.stations for s in station.get_sprites(g, sprites)]
        )

    @property
    def sprites(self):
        return [*dict.fromkeys([sub for s in self.stations for sub in s.sprites])]
