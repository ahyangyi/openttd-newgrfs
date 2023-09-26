def check_reachability(economy):
    can_be_produced = set()
    while True:
        changed = False

        for industry in economy.graph.values():
            i = industry.consumes
            o = industry.produces
            if all(x in can_be_produced for x in i):
                for x in o:
                    if x not in can_be_produced:
                        can_be_produced.add(x)
                        changed = True

        if not changed:
            break

    assert len(can_be_produced) == len(
        economy.cargos
    ), f"The following cargos can be produced: {', '.join(str(x) for x in can_be_produced)}, and the following cargos cannot: {', '.join(str(x) for x in economy.cargos if x not in can_be_produced)}"
