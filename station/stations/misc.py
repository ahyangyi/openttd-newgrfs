import grf
from station.lib import ADefaultGroundSprite, ALayout
from station.lib.registers import Registers

track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
track = ALayout([track_ground], [], True)
