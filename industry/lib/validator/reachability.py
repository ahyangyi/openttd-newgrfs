def check_reachability(economy):
    can_produce = set()
    while True:
        changed = False

        for industry in economy.graph.values():
            i = industry.consumes
            o = industry.produces
            if all(x in can_produce for x in i):
                for x in o:
                    if x not in can_produce:
                        can_produce.add(x)
                        changed = True

        if not changed:
            break

    assert len(can_produce) == len(
        economy.cargos
    ), f"The following cargos can be produced: {', '.join(str(x) for x in can_produce)}, and the following cargos cannot: {', '.join(str(x) for x in economy.cargos if x not in can_produce)}"

    can_accept = set()
    for industry in economy.graph.values():
        can_accept.update(industry.accepts)

    assert can_produce.issubset(
        can_accept
    ), f"The following cargos can be produced but not accepted by any industry: {', '.join(str(x) for x in can_produce if x not in can_accept)}"
