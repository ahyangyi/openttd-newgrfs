def check_reachability(economy):
    can_be_produced = set()
    while True:
        changed = False

        for i, o in economy.graph.values():
            if all(x in can_be_produced for x in i):
                for x in o:
                    if x not in can_be_produced:
                        can_be_produced.add(x)
                        changed = True

        if not changed:
            break

    assert len(can_be_produced) == len(economy.cargos)
