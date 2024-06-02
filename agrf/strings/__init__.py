from nml import grfstrings


def get_translation(stringref, lang_id=0x7F):
    stringref.manager.set_nml_globals()
    ns = stringref.string_nmlexpr
    if lang_id in grfstrings.get_translations(ns):
        return grfstrings.get_translation(ns, lang_id)
    return grfstrings.get_translation(ns)

def remove_control_letters(s):
    ret = []
    i = 0
    while i < len(s):
        if s[i] == "\\":
            if s[i + 1] == "U":
                i += 6
            else:
                i += 3
        else:
            ret.append(s[i])
            i += 1
    return "".join(ret)
