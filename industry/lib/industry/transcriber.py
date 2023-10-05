def transcribe_one(pattern, registry):
    ret = []
    for i, r in enumerate(pattern):
        for j, c in enumerate(r):
            if c != " ":
                ret.append({"xofs": i, "yofs": j, "gfx": registry[c]})
    return ret


def transcribe(patterns, registry):
    return [transcribe_one(p, registry) for p in patterns]
