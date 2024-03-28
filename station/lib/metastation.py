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
        for station in self.stations:
            g.add(station)
