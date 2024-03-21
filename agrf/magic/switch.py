import grf


class Switch(grf.Switch):
    def __init__(self, code, ranges, default, *, feature=None, ref_id=None, related_scope=False, subroutines=None):
        super().__init__(
            code, ranges, default, feature=feature, ref_id=ref_id, related_scope=related_scope, subroutines=subroutines
        )

    def __getattr__(self, name):
        call = lambda x: getattr(x, name)
        new_ranges = {(r.low, r.high): call(r.ref) for r in self._ranges}
        new_default = call(self.default)
        return Switch(
            self.code,
            new_ranges,
            new_default,
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
        )

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ranges = {(r.low, r.high): call(r.ref) for r in self._ranges}
        new_default = call(self.default)
        return Switch(
            self.code,
            new_ranges,
            new_default,
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
        )
