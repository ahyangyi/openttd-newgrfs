def check_yeti(economy):
    if economy.parameters["WORKFORCE"] in ("YETI", "YETI_PASSENGERS", "YETI_MAIL", "YETI_TIRED"):
        assert any(x.name == "Worker Yard" for x in economy.industries)
