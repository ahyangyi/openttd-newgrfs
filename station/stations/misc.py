import grf
from station.lib import ADefaultGroundSprite, AGroundSprite, ALayout
from station.lib.registers import Registers

track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
road_ground = ADefaultGroundSprite(1314)
default_ground = ADefaultGroundSprite(3981, flags={"add": Registers.CLIMATE_OFFSET})
building_ground = ADefaultGroundSprite(1420, flags={"add": Registers.ZERO})
empty_ground = AGroundSprite(grf.EMPTY_SPRITE, flags={"add": Registers.ZERO})

track = ALayout(track_ground, [], True)
default = ALayout(default_ground, [], False)
