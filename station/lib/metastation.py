import grf
from .utils import class_label_printable
from .station import AStation


class AMetaStation(grf.SpriteGenerator):
    def __init__(self, stations, class_label, categories, demos, road_stops=None, objects=None):
        super().__init__()
        self.stations = stations
        self.class_label = class_label
        self.categories = categories
        self.demos = demos
        self.road_stops = road_stops or []
        self.objects = objects or []

    @property
    def class_label_plain(self):
        return class_label_printable(self.class_label)

    def check_id_uniqueness(self):
        ids = [x.id for x in self.stations]
        assert len(ids) == len(
            set(ids)
        ), f"ID 0x{[x for x in ids if ids.count(x) > 1][0]:x} occurs twice! {[hex(x) for x in ids]}"

    def remap(self, station_idmap):
        for station in self.stations:
            if station.id in station_idmap:
                station.id = station_idmap[station.id]

    def get_sprites(self, g):
        sprites = self.sprites

        ret = [grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(sprites))] + sprites

        for station in self.stations:
            ret.extend(station.get_sprites(g, sprites))
        for road_stop in self.road_stops:
            ret.extend(road_stop.get_sprites(g))
        for obj in self.objects:
            ret.extend(obj.get_sprites(g))
        return ret

    @property
    def sprites(self):
        return [*dict.fromkeys([sub for s in self.stations for sub in s.sprites])]
