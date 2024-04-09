import grf
from .utils import class_label_printable


class AMetaStation:
    def __init__(self, stations, class_label, categories, doc_layouts, demos):
        self.stations = stations
        self.class_label = class_label
        self.categories = categories
        self.doc_layouts = doc_layouts
        self.demos = demos

    @property
    def class_label_plain(self):
        return class_label_printable(self.class_label)

    def add(self, g):
        g.add(grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(self.stations[0].sprites)))
        for s in self.stations[0].sprites:
            g.add(s)
        for station in self.stations:
            g.add(station)
