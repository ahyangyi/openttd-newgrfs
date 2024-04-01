class BinaryVariantMixin:
    @classmethod
    def create_variants(classobj, variants):
        for i, v in enumerate(variants):
            cls = v.__class__
            v.__class__ = type(cls.__name__, (classobj, cls), {})
            v.M = variants[i ^ classobj._m_offset]
            v.R = variants[i ^ classobj._r_offset]
            v.T = variants[i ^ classobj._t_offset]
        return variants[0]

    @classmethod
    def get_all_variants(cls, thing):
        ret = [thing]
        if cls._r_offset > 0:
            ret = ret + [x.R for x in ret]
        if cls._t_offset > cls._r_offset:
            ret = ret + [x.T for x in ret]
        if cls._m_offset > 0:
            ret = [y for x in ret for y in [x, x.M]]
        return ret

    @property
    def all_variants(self):
        return self.get_all_variants(self)

    @property
    def TR(self):
        return self.T.R

    @classmethod
    def is_symmetrical_y(classobj):
        return classobj._t_offset == 0


class BuildingSpriteSheetFull(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def render_indices():
        return list(range(8))

    _m_offset = 1
    _r_offset = 2
    _t_offset = 4


class BuildingSpriteSheetSymmetricalX(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def render_indices():
        return [0, 1, 4, 5]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 2


class BuildingSpriteSheetSymmetricalY(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 0


class BuildingSpriteSheetSymmetrical(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def render_indices():
        return [0, 1]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 0


class BuildingSpriteSheetRotational(BinaryVariantMixin):
    def __init__(self, obj):
        super().__init__(obj)

    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 2
