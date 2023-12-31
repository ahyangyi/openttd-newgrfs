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

    can_accept = set()
    for industry in economy.graph.values():
        can_accept.update(industry.accepts)

    assert can_produce.issubset(
        can_accept
    ), f"The following cargos can be produced but not accepted by any industry: {', '.join(str(x) for x in can_produce if x not in can_accept)}"

    assert can_accept.issubset(
        can_produce
    ), f"The following cargos can be accepted but not produced by any industry: {', '.join(str(x) for x in can_accept if x not in can_produce)}"
