def h_merge(layouts, sep):
    ret = []
    for r in range(len(sep)):
        cur_row = []
        for i, l in enumerate(layouts):
            if i > 0:
                cur_row.extend(sep[r])
            cur_row.extend(l[r])
        ret.append(cur_row)
    return ret
