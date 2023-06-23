import grf

OPEN_CARGO_CLASSES = (
    grf.CargoClass.BULK
    | grf.CargoClass.PIECE_GOODS
    | grf.CargoClass.EXPRESS
    | grf.CargoClass.LIQUID
    | grf.CargoClass.ARMOURED
    | grf.CargoClass.REFRIGERATED
    | grf.CargoClass.COVERED
    | grf.CargoClass.OVERSIZED
    | grf.CargoClass.NON_POURABLE
)

TANKER_CARGO_CLASSES = grf.CargoClass.LIQUID

TARPAULIN_CARGO_CLASSES = (
    grf.CargoClass.BULK
    | grf.CargoClass.PIECE_GOODS
    | grf.CargoClass.EXPRESS
    | grf.CargoClass.LIQUID
    | grf.CargoClass.ARMOURED
    | grf.CargoClass.REFRIGERATED
    | grf.CargoClass.COVERED
    | grf.CargoClass.OVERSIZED
    | grf.CargoClass.NON_POURABLE
    | grf.CargoClass.MAIL
)
