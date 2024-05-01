def h_merge(layouts, sep):
    return [[c for cols, s in zip(r, [sep] * len(r)) for c in cols + s][: -len(sep)] for r in zip(*layouts)]
