from agrf.magic import Switch
from agrf.utils import unique_tuple


class GraphicalSwitch(Switch):
    def __init__(self, code, ranges, default, *, feature=None, ref_id=None, related_scope=False, subroutines=None):
        super().__init__(
            code, ranges, default, feature=feature, ref_id=ref_id, related_scope=related_scope, subroutines=subroutines
        )

    @property
    def sprites(self):
        return unique_tuple([s for sw in [self.default] + [r.ref for r in self._ranges] for s in sw.sprites])
