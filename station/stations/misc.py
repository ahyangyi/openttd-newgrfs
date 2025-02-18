from station.lib import ADefaultGroundSprite, ALayout
from station.lib.registers import Registers

track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
road_ground = ADefaultGroundSprite(1314)
road_ground_turn = ADefaultGroundSprite(1321)
default_ground = ADefaultGroundSprite(3981, flags={"add": Registers.CLIMATE_OFFSET})
slope_1_ground = ADefaultGroundSprite(3989, flags={"add": Registers.CLIMATE_OFFSET})
slope_2_ground = ADefaultGroundSprite(3990, flags={"add": Registers.CLIMATE_OFFSET})
slope_3_ground = ADefaultGroundSprite(3994, flags={"add": Registers.CLIMATE_OFFSET})
building_ground = ADefaultGroundSprite(1420, flags={"add": Registers.ZERO})

track = ALayout(track_ground, [], True)
default = ALayout(default_ground, [], False)
slope_1 = ALayout(slope_1_ground, [], False)
slope_2 = ALayout(slope_2_ground, [], False)
slope_3 = ALayout(slope_3_ground, [], False)
building_ground_layout = ALayout(building_ground, [], False)
road_ground_turn_layout = ALayout(road_ground_turn, [], False)
