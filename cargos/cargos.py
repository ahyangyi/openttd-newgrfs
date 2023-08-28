from agrf.graphics.recolour import ColourRange, ColourMap

# Cargo list forked from polar_fox
# Colour maps from TimberWolf
cargo_info = {
    "PASS": {},
    "TOUR": {},
    "MAIL": {},
    "COAL": {},
    "IORE": {
        "COAL": ColourMap(
            "iron-ore",
            [(ColourRange(3, 8), ColourRange(75, 80))],
        )
    },
    "GRVL": {
        "COAL": ColourMap(
            "gravel",
            [
                (ColourRange(3, 3), ColourRange(18, 18)),
                (ColourRange(4, 4), ColourRange(57, 57)),
                (ColourRange(5, 5), ColourRange(20, 20)),
                (ColourRange(6, 6), ColourRange(58, 58)),
                (ColourRange(7, 8), ColourRange(22, 23)),
            ],
        )
    },
    "SAND": {},
    "AORE": {},
    "CORE": {
        "COAL": ColourMap(
            "copper",
            [(ColourRange(3, 8), ColourRange(72, 77))],
        )
    },
    "CLAY": {},
    "SCMT": {},
    "WOOD": {},
    "LIME": {},
    "GOOD": {},
    "FOOD": {},
    "STEL": {},
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
    "GRAI": {
        "COAL": ColourMap(
            "grain",
            [(ColourRange(3, 8), ColourRange(34, 39))],
        )
    },
    "LVST": {},
    "MAIZ": {},
    "MILK": {},
    "RUBR": {},
    "SGBT": {},
    "SGCN": {},
    "WHEA": {
        "COAL": ColourMap(
            "wheat",
            [(ColourRange(3, 8), ColourRange(116, 121))],
        )
    },
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
    "POTA": {},
    "PORE": {},
    "IRON": {},
    "NICK": {},
    "SLAG": {},
    "QLME": {},
    "BOOM": {},
    "METL": {},
    "SULP": {},
    "SASH": {},
    "CMNT": {},
    "COKE": {},
    "KAOL": {},
    "FERT": {},
    "PIPE": {},
    "SALT": {},
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
}

cargos = list(cargo_info.keys())


assert len(cargos) == len(set(cargos))
