def check_climate_supplies(economy):
    if economy.parameters["TOWN_GOODS"] in ("FOOD", "FOOD_AND_WATER"):
        assert any(x.label == b"FOOD" for x in economy.cargos)
    if economy.parameters["TOWN_GOODS"] == "FOOD_AND_WATER":
        assert any(x.label == b"WATR" for x in economy.cargos)
