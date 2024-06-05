import grf
from station.lib import ADefaultGroundSprite, AGroundSprite, ALayout
from station.lib.registers import Registers

track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
default_ground = ADefaultGroundSprite(3981, flags={"add": Registers.CLIMATE_OFFSET})
empty_ground = AGroundSprite(grf.EMPTY_SPRITE, flags={"add": Registers.CLIMATE_RAIL_OFFSET})

track = ALayout([track_ground], [], True)
default = ALayout([default_ground], [], False)
