import grf
from collections.abc import Collection, Mapping, Hashable


def deep_freeze(thing):
    if thing is None or isinstance(thing, str):
        return thing
    elif isinstance(thing, Mapping):
        return tuple((k, deep_freeze(v)) for k, v in sorted(thing.items()))
    elif isinstance(thing, Collection):
        return tuple(deep_freeze(i) for i in thing)
    elif not isinstance(thing, Hashable):
        raise TypeError(f"unfreezable type: '{type(thing)}'")
    else:
        return thing


class Switch(grf.Switch):
    def __init__(self, code, ranges, default, *, feature=None, ref_id=None, related_scope=False, subroutines=None):
        super().__init__(
            code, ranges, default, feature=feature, ref_id=ref_id, related_scope=related_scope, subroutines=subroutines
        )
        self.attr_cache = {}
        self.call_cache = {}

    def derive(self, callback):
        return Switch(
            self.code,
            {(r.low, r.high): callback(r.ref) for r in self._ranges},
            callback(self.default),
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
        )

    def __getattr__(self, name):
        if name in self.attr_cache:
            return self.attr_cache[name]
        ret = self.derive(lambda x: getattr(x, name))
        self.attr_cache[name] = ret
        return ret

    def __call__(self, *args, **kwargs):
        key = deep_freeze((args, kwargs))
        if key in self.call_cache:
            return self.call_cache[key]
        ret = self.derive(lambda x: x(*args, **kwargs))
        self.call_cache[key] = ret
        return ret

    # FIXME: should probably be refactored into something more general
    # and not rely on everything else implementing `get_default_graphics`
    # But that'll happen after LazyVoxel refactor
    def get_default_graphics(self):
        return self.default.get_default_graphics()
