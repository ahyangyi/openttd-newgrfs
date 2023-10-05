def flip(pattern):
    return tuple(str(x[::-1]) for x in pattern)


def rotate(pattern):
    return tuple("".join(x) for x in list(zip(*pattern))[::-1])


def symmetrize_one(pattern):
    ret = []
    for x in range(4):
        ret.append(pattern)
        ret.append(flip(pattern))
        pattern = rotate(pattern)
    return ret


def unique(patterns):
    return list(set(patterns))


def symmetrize(patterns):
    return unique(sum(map(symmetrize_one, patterns), start=[]))
