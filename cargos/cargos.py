from agrf.graphics.recolour import ColourRange, ColourMap

# Cargo list forked from polar_fox
# Some colour maps from TimberWolf:
cargo_info = {
    "PASS": {},
    "TOUR": {},
    "MAIL": {},
    "COAL": {},
    "IORE": {"COAL": ColourMap("iron-ore", [(ColourRange(3, 8), ColourRange(75, 80))])},
    "GRVL": {
        "COAL": ColourMap(
            "gravel",
            [
                (ColourRange(3), ColourRange(18)),
                (ColourRange(4), ColourRange(57)),
                (ColourRange(5), ColourRange(20)),
                (ColourRange(6), ColourRange(58)),
                (ColourRange(7, 8), ColourRange(22, 23)),
            ],
        )
    },
    "SAND": {"COAL": ColourMap("sand", [(ColourRange(3, 8), ColourRange(55, 60))])},
    "AORE": {},
    "CORE": {"COAL": ColourMap("copper", [(ColourRange(3, 8), ColourRange(72, 77))])},
    "CLAY": {},
    "SCMT": {},
    "WOOD": {},
    "LIME": {},
    "GOOD": {},
    "FOOD": {},
    "STEL": {},
    "VALU": {},
    "GOLD": {},
    "DIAM": {},
    "FMSP": {},
    "ENSP": {},
    "BEER": {},
    "BDMT": {},
    "MNSP": {},
    "PAPR": {},
    "WDPR": {},
    "COPR": {},
    "DYES": {},
    "OIL_": {},
    "RFPR": {},
    "PETR": {},
    "PLAS": {},
    "WATR": {},
    "FISH": {},
    "CERE": {},
    "FICR": {},
    "FRVG": {},
    "FRUT": {},
    "GRAI": {"COAL": ColourMap("grain", [(ColourRange(3, 8), ColourRange(34, 39))])},
    "LVST": {},
    "MAIZ": {},
    "MILK": {},
    "RUBR": {},
    "SGBT": {},
    "SGCN": {},
    "WHEA": {"COAL": ColourMap("wheat", [(ColourRange(3, 8), ColourRange(116, 121))])},
    "WOOL": {},
    "OLSD": {},
    "SUGR": {},
    "JAVA": {},
    "BEAN": {},
    "NITR": {},
    "VEHI": {},
    "EOIL": {},
    "NUTS": {},
    "CASS": {},
    "MNO2": {},
    "PHOS": {},
    "POTA": {"COAL": ColourMap("potash", [(ColourRange(3, 8), ColourRange(45, 50))])},
    "PORE": {
        "COAL": ColourMap(
            "pyrite ore",
            [(ColourRange(4), ColourRange(38)), (ColourRange(6), ColourRange(55)), (ColourRange(8), ColourRange(53))],
        )
    },
    "IRON": {},
    "NICK": {},
    "SLAG": {},
    "QLME": {},
    "BOOM": {},
    "METL": {},
    "SULP": {"COAL": ColourMap("sulphur", [(ColourRange(3, 8), ColourRange(68, 73))])},
    "SASH": {},
    "CMNT": {},
    "COKE": {},
    "KAOL": {
        "COAL": ColourMap(
            "kaolin",
            [
                (ColourRange(3), ColourRange(0x79)),
                (ColourRange(4), ColourRange(0x79)),
                (ColourRange(5), ColourRange(0x7A)),
                (ColourRange(6), ColourRange(0x7A)),
                (ColourRange(7), ColourRange(0x7B)),
                (ColourRange(8), ColourRange(0x7B)),
            ],
        )
    },
    "FERT": {},
    "PIPE": {},
    "SALT": {
        "COAL": ColourMap(
            "salt",
            [
                (ColourRange(3), ColourRange(11)),
                (ColourRange(4, 5), ColourRange(0x87, 0x88)),
                (ColourRange(6, 8), ColourRange(14, 16)),
            ],
        )
    },
    "CBLK": {},
    "CHLO": {},
    "VPTS": {},
    "ACID": {},
    "ALUM": {},
    "CTCD": {},
    "TOFF": {},
    "URAN": {},
    "CTAR": {},
    "O2__": {},
    "STAL": {},
    "STCB": {},
    "STST": {},
    "CSTI": {},
    "PEAT": {},
    "ZINC": {},
    "TYRE": {},
    "VBOD": {},
    "VENG": {},
    "FECR": {},
    "GLAS": {},
    "POWR": {},
    "STSH": {},
    "STWR": {},
    "NH3_": {},
    "STSE": {},
    "SEED": {},
    "TATO": {},
    "WDCH": {},
    "BAKE": {},
    # Start of our addition
    # ECS
    "BRCK": {},
    "CERA": {},
    # ITI
    "NUKF": {},
    "NUKW": {},
    "WSTE": {},
    # Caribbean
    "CIGR": {},
    "COBL": {},
    "MOLS": {},
    "OILI": {},
    "OILD": {},
    "TBCO": {},
    # YETI
    "YETI": {},
    "YETY": {},
    # OTIS
    "OTI1": {},
    "OTI2": {},
    # AEGIS
    "WRKR": {},
    "TRWK": {},
}

voxel_map = {"COAL": "coal"}


def make_voxel_remap():
    voxel_remap = {}
    for k, v in cargo_info.items():
        for source, remap in v.items():
            if source in voxel_map:
                voxel_remap[k] = (source, remap)
    return voxel_remap


voxel_remap = make_voxel_remap()

cargo_info = {k.encode(): v for k, v in cargo_info.items()}
cargos = list(cargo_info.keys())


assert len(cargos) == len(set(cargos))
