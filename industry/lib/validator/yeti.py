def check_yeti(economy):
    if economy.parameters["WORKER"] in ("YETI", "YETI_PASSENGERS", "YETI_MAIL", "YETI_TIRED_WORKER"):
        assert any(x.name == "Worker Yard" for x in economy.industries)
