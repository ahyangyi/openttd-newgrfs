class BuildingSymmetryMixin:
    @classmethod
    def create_variants(classobj, variants):
        for i, v in enumerate(variants):
            cls = v.__class__
            v.__class__ = type(cls.__name__ + "+" + classobj.__name__, (cls, classobj), {})
            if classobj._m_offset == 0:
                v.M = variants[i ^ 3 if i in [1, 2] else i]
            else:
                v.M = variants[i ^ classobj._m_offset]
            v.R = variants[i ^ classobj._r_offset]
            v.T = variants[i ^ classobj._t_offset]
            v.symmetry = classobj
        return variants[0]

    # FIXME this is actually wrong for "weird" symmetries
    @classmethod
    def get_all_variants(cls, thing):
        ret = cls.get_all_entries(thing)
        if cls._m_offset > 0:
            ret = [y for x in ret for y in [x, x.M]]
        return ret

    @classmethod
    def get_all_entries(cls, thing):
        ret = [thing]
        if cls._r_offset > 0:
            ret = ret + [x.R for x in ret]
        if cls._t_offset > cls._r_offset:
            ret = ret + [x.T for x in ret]
        return ret

    @property
    def all_variants(self):
        return self.get_all_variants(self)

    def fmap(self, f):
        mapped = list(map(f, self.all_variants))
        cls = self.__class__.__bases__[0]
        return cls.create_variants(mapped)

    @classmethod
    def is_symmetrical_y(classobj):
        return classobj._t_offset == 0


class BuildingFull(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return list(range(8))

    _m_offset = 1
    _r_offset = 2
    _t_offset = 4

    @classmethod
    def break_x_symmetry(classobj):
        return classobj

    @classmethod
    def break_y_symmetry(classobj):
        return classobj

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetricalY


class BuildingSymmetricalX(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return [0, 1, 4, 5]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 2

    @classmethod
    def break_x_symmetry(classobj):
        return BuildingFull

    @classmethod
    def break_y_symmetry(classobj):
        return classobj

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetrical


class BuildingSymmetricalY(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 0

    @classmethod
    def break_x_symmetry(classobj):
        return BuildingSymmetricalY

    @classmethod
    def break_y_symmetry(classobj):
        return BuildingFull

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetricalY


class BuildingSymmetrical(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return [0, 1]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 0

    @classmethod
    def break_x_symmetry(classobj):
        return BuildingSymmetricalY

    @classmethod
    def break_y_symmetry(classobj):
        return BuildingSymmetricalX

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetrical


class BuildingRotational(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 2

    @classmethod
    def break_x_symmetry(classobj):
        return BuildingFull

    @classmethod
    def break_y_symmetry(classobj):
        return BuildingFull

    @classmethod
    def add_y_symmetry(classobj):
        # FIXME more symmetrical than this?
        return BuildingSymmetrical


class BuildingDiagonal(BuildingSymmetryMixin):
    @staticmethod
    def render_indices():
        return [0, 2, 4, 6]

    _m_offset = 0
    _r_offset = 1
    _t_offset = 2

    @classmethod
    def break_x_symmetry(classobj):
        return BuildingFull

    @classmethod
    def break_y_symmetry(classobj):
        return BuildingFull

    @classmethod
    def add_y_symmetry(classobj):
        # FIXME more symmetrical than this?
        return BuildingSymmetrical
