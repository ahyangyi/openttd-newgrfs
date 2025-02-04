import grf
from station.lib import ADefaultGroundSprite, AGroundSprite, ALayout
from station.lib.registers import Registers
from agrf.lib.building.default import empty_ground

track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
road_ground = ADefaultGroundSprite(1314)
road_ground_w = ADefaultGroundSprite(1320)
road_ground_n = ADefaultGroundSprite(1321)
default_ground = ADefaultGroundSprite(3981, flags={"add": Registers.CLIMATE_OFFSET})
building_ground = ADefaultGroundSprite(1420, flags={"add": Registers.ZERO})

track = ALayout(track_ground, [], True)
default = ALayout(default_ground, [], False)
building_ground_layout = ALayout(building_ground, [], False)
road_ground_w_layout = ALayout(road_ground_w, [], False)
road_ground_n_layout = ALayout(road_ground_n, [], False)
