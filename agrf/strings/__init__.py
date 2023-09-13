from nml import grfstrings


def get_translation(stringref, lang_id=0x7F):
    stringref.manager.set_nml_globals()
    ns = stringref.string_nmlexpr
    if lang_id in grfstrings.get_translations(ns):
        return grfstrings.get_translation(ns, lang_id)
    return grfstrings.get_translation(ns)
