from .industry_desc import WorkerYard
from industry.cargos import mail, passengers, tired_workers, workers
from industry.industries import worker_yard


class WorkerMixin:
    @staticmethod
    def default_worker_support(economy, yeti_boosters, special_destinations, primary_industries, secondary_industries):
        parameters = economy.parameters
        if parameters["WORKFORCE"].startswith("YETI"):
            if parameters["WORKFORCE"] == "YETI":
                economy.graph[worker_yard] = WorkerYard(workers, boosters=yeti_boosters)
            elif parameters["WORKFORCE"] == "YETI_PASSENGERS":
                economy.graph[worker_yard] = WorkerYard(workers, boosters=yeti_boosters + (passengers,))
            elif parameters["WORKFORCE"] == "YETI_MAIL":
                economy.graph[worker_yard] = WorkerYard(workers, boosters=yeti_boosters + (mail,))
            elif parameters["WORKFORCE"] == "YETI_TIRED":
                economy.graph[worker_yard] = WorkerYard(workers, boosters=yeti_boosters + (tired_workers,))

            # FIXME: remove PRESET
            if parameters["WORKER_PARTICIPATION"] in ("PRESET", "NONE"):
                for ind in special_destinations:
                    economy.graph[ind].boosters += (workers,)
                    if parameters["WORKFORCE"] == "YETI_TIRED":
                        economy.graph[ind].produces += (tired_workers,)
            if parameters["WORKER_PARTICIPATION"] in ("PRIMARY_INDUSTRY", "BOTH"):
                for i in primary_industries:
                    if i in economy.graph:
                        economy.graph[i] = economy.graph[i].to_secondary(workers)
                        if parameters["WORKFORCE"] == "YETI_TIRED":
                            economy.graph[i].produces += (tired_workers,)
            if parameters["WORKER_PARTICIPATION"] in ("SECONDARY_INDUSTRY", "BOTH"):
                for i in secondary_industries:
                    if i in economy.graph:
                        economy.graph[i].boosters += (workers,)
                        if parameters["WORKFORCE"] == "YETI_TIRED":
                            economy.graph[i].produces += (tired_workers,)
