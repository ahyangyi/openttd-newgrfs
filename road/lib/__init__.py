from agrf.lib.road_type import RoadType


class ARoadType(RoadType):
    def __init__(self, *, id, underlay, **props):
        super().__init__(id=id, underlay=underlay, **props)
