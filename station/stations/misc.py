import grf
from station.lib import ADefaultGroundSprite, ALayout

track_ground = ADefaultGroundSprite(1012, {"add": grf.Temp(0)})
track = ALayout([track_ground], [], True)
