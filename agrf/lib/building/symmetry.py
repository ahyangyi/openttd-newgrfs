class BuildingSymmetryMixin:
    @classmethod
    def create_variants(classobj, variants):
        for i, v in enumerate(variants):
            cls = v.__class__
            v.__class__ = type(cls.__name__, (cls, classobj), {})
            if classobj._m_offset == 0:
                v.M = variants[i ^ 3 if i in [1, 2] else i]
            else:
                v.M = variants[i ^ classobj._m_offset]
            v.R = variants[i ^ classobj._r_offset]
            v.T = variants[i ^ classobj._t_offset]
            v.symmetry = classobj
        return variants[0]

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

    @classmethod
    def is_symmetrical_y(classobj):
        return classobj._t_offset == 0

    @staticmethod
    def __canonicalize_descriptor(descriptor):
        ret = []
        assignment = {}
        for x in descriptor:
            if x not in assignment:
                assignment[x] = len(assignment)
            ret.append(assignment[x])
        return tuple(ret)

    @classmethod
    def break_x_symmetry(classobj):
        new_descriptor = tuple(x + d for x, d in zip(classobj._symmetry_descriptor, (0, 0, 8, 8, 0, 0, 8, 8)))
        new_descriptor = BuildingSymmetryMixin.__canonicalize_descriptor(new_descriptor)
        return BuildingSymmetryMixin._type_pool[new_descriptor]

    @classmethod
    def break_y_symmetry(classobj):
        new_descriptor = tuple(x + d for x, d in zip(classobj._symmetry_descriptor, (0, 0, 0, 0, 8, 8, 8, 8)))
        new_descriptor = BuildingSymmetryMixin.__canonicalize_descriptor(new_descriptor)
        return BuildingSymmetryMixin._type_pool[new_descriptor]

    _type_pool = {}


class BuildingFull(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 4, 5, 6, 7)

    @staticmethod
    def render_indices():
        return list(range(8))

    _m_offset = 1
    _r_offset = 2
    _t_offset = 4

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetricalY


class BuildingSymmetricalX(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 0, 1, 2, 3, 2, 3)

    @staticmethod
    def render_indices():
        return [0, 1, 4, 5]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 2

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetrical


class BuildingSymmetricalY(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 0, 1, 2, 3)

    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 0

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetricalY


class BuildingSymmetrical(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 0, 1, 0, 1, 0, 1)

    @staticmethod
    def render_indices():
        return [0, 1]

    _m_offset = 1
    _r_offset = 0
    _t_offset = 0

    @classmethod
    def add_y_symmetry(classobj):
        return BuildingSymmetrical


class BuildingRotational(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 2, 3, 0, 1)

    @staticmethod
    def render_indices():
        return [0, 1, 2, 3]

    _m_offset = 1
    _r_offset = 2
    _t_offset = 2

    @classmethod
    def add_y_symmetry(classobj):
        # FIXME more symmetrical than this?
        return BuildingSymmetrical


class BuildingDiagonal(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 0, 1, 2, 2, 1, 3, 3)

    @staticmethod
    def render_indices():
        return [0, 2, 4, 6]

    _m_offset = 0
    _r_offset = 1
    _t_offset = 2

    @classmethod
    def add_y_symmetry(classobj):
        # FIXME more symmetrical than this?
        return BuildingSymmetrical


class BuildingCylindrical(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 0, 0, 0, 0, 0, 0, 0)

    @staticmethod
    def render_indices():
        return [0]

    _m_offset = 0
    _r_offset = 0
    _t_offset = 0

    @classmethod
    def break_x_symmetry(classobj):
        raise NotImplemented()

    @classmethod
    def break_y_symmetry(classobj):
        raise NotImplemented()

    @classmethod
    def add_y_symmetry(classobj):
        raise NotImplemented()


BuildingSymmetryMixin._type_pool[(0, 1, 2, 3, 4, 5, 6, 7)] = BuildingFull
BuildingSymmetryMixin._type_pool[(0, 1, 0, 1, 2, 3, 2, 3)] = BuildingSymmetricalX
BuildingSymmetryMixin._type_pool[(0, 1, 2, 3, 0, 1, 2, 3)] = BuildingSymmetricalY
BuildingSymmetryMixin._type_pool[(0, 1, 0, 1, 0, 1, 0, 1)] = BuildingSymmetrical
