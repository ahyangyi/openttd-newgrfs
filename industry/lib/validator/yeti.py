from industry.lib.economy import WorkerYard
from industry.industries import worker_yard


def check_yeti(economy):
    if economy.parameters["WORKFORCE"] in ("YETI", "YETI_PASSENGERS", "YETI_MAIL", "YETI_TIRED"):
        assert worker_yard in economy.industries

        conf = economy.graph[worker_yard]
        assert isinstance(conf, WorkerYard)

        if economy.parameters["WORKFORCE"] == "YETI":
            assert len(conf.boosters) == 2
        else:
            assert len(conf.boosters) == 3
