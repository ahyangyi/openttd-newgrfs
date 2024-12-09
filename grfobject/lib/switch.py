import grf
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


class PositionSwitch(GraphicalSwitch):
    def __init__(
        self,
        code,
        ranges,
        default,
        *,
        feature=None,
        ref_id=None,
        related_scope=False,
        subroutines=None,
        rows=1,
        columns=1
    ):
        super().__init__(
            code, ranges, default, feature=feature, ref_id=ref_id, related_scope=related_scope, subroutines=subroutines
        )
        self.rows = rows
        self.columns = columns

    def fmap(self, f):
        return type(self)(
            self.code,
            {(r.low, r.high): f(r.ref) for r in self._ranges},
            f(self.default),
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
            rows=self.rows,
            columns=self.columns,
        )

    def to_lists(self):
        return [[self.lookup(r * 256 + self.columns - 1 - c) for c in range(self.columns)] for r in range(self.rows)]

    @staticmethod
    def __index_M(p):
        x, y = p // 256, p % 256
        return y * 256 + x

    @property
    def M(self):
        return type(self)(
            self.code,
            {self.__index_M(p): r.ref.M for r in self._ranges for p in range(r.low, r.high + 1)},
            self.default.M,
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
            rows=self.columns,
            columns=self.rows,
        )

    @staticmethod
    def __index_R(p, c):
        x, y = p // 256, p % 256
        return x * 256 + (c - 1 - y)

    @property
    def R(self):
        return type(self)(
            self.code,
            {self.__index_R(p, self.columns): r.ref.R for r in self._ranges for p in range(r.low, r.high + 1)},
            self.default.R,
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
            rows=self.rows,
            columns=self.columns,
        )

    @staticmethod
    def __index_T(p, r):
        x, y = p // 256, p % 256
        return (r - x - 1) * 256 + y

    @property
    def T(self):
        return type(self)(
            self.code,
            {self.__index_T(p, self.rows): r.ref.T for r in self._ranges for p in range(r.low, r.high + 1)},
            self.default.T,
            feature=self.feature,
            ref_id=self.ref_id,
            related_scope=self.related_scope,
            subroutines=self.subroutines,
            rows=self.rows,
            columns=self.columns,
        )
