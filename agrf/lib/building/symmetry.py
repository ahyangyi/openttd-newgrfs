class BuildingSymmetryMixin:
    @classmethod
    def create_variants(classobj, variants):
        for i, v in enumerate(variants):
            cls = v.__class__
            v.__class__ = type(cls.__name__, (cls, classobj), {})

            idx = classobj.render_indices()[i]
            v.M = variants[classobj._symmetry_descriptor[idx ^ 1]]
            v.R = variants[classobj._symmetry_descriptor[idx ^ 2]]
            v.T = variants[classobj._symmetry_descriptor[idx ^ 4]]
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

    @staticmethod
    def __merge_descriptor(descriptor, merge_operations):
        assignment = {}
        for a, b in merge_operations:
            while a in assignment:
                a = assignment[a]
            while b in assignment:
                b = assignment[b]
            if a == b:
                continue
            if a < b:
                assignment[b] = a
            else:
                assignment[a] = b

        ret = []
        for x in descriptor:
            while x in assignment:
                x = assignment[x]
            ret.append(x)
        return tuple(ret)

    @classmethod
    def render_indices(classobj):
        ret = []
        seen = set()
        for i in range(8):
            if classobj._symmetry_descriptor[i] not in seen:
                seen.add(classobj._symmetry_descriptor[i])
                ret.append(i)

        return ret

    @classmethod
    def join(classobj1, classobj2):
        new_descriptor = tuple((classobj1._symmetry_descriptor[i], classobj2._symmetry_descriptor[i]) for i in range(8))
        new_descriptor = BuildingSymmetryMixin.__canonicalize_descriptor(new_descriptor)
        return BuildingSymmetryMixin._type_pool[new_descriptor]

    @classmethod
    def break_x_symmetry(classobj):
        return classobj.join(BuildingSymmetricalY)

    @classmethod
    def break_y_symmetry(classobj):
        return classobj.join(BuildingSymmetricalX)

    @classmethod
    def add_x_symmetry(classobj):
        new_descriptor = BuildingSymmetryMixin.__merge_descriptor(
            classobj._symmetry_descriptor,
            [
                (classobj._symmetry_descriptor[a], classobj._symmetry_descriptor[b])
                for a, b in [(0, 2), (1, 3), (4, 6), (5, 7)]
            ],
        )
        new_descriptor = BuildingSymmetryMixin.__canonicalize_descriptor(new_descriptor)
        return BuildingSymmetryMixin._type_pool[new_descriptor]

    @classmethod
    def add_y_symmetry(classobj):
        new_descriptor = BuildingSymmetryMixin.__merge_descriptor(
            classobj._symmetry_descriptor,
            [
                (classobj._symmetry_descriptor[a], classobj._symmetry_descriptor[b])
                for a, b in [(0, 4), (1, 5), (2, 6), (3, 7)]
            ],
        )
        new_descriptor = BuildingSymmetryMixin.__canonicalize_descriptor(new_descriptor)
        return BuildingSymmetryMixin._type_pool[new_descriptor]

    _type_pool = {}


class BuildingFull(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 4, 5, 6, 7)

    _m_offset = 1
    _r_offset = 2
    _t_offset = 4


class BuildingSymmetricalX(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 0, 1, 2, 3, 2, 3)

    _m_offset = 1
    _r_offset = 0
    _t_offset = 2


class BuildingSymmetricalY(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 0, 1, 2, 3)

    _m_offset = 1
    _r_offset = 2
    _t_offset = 0


class BuildingSymmetrical(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 0, 1, 0, 1, 0, 1)

    _m_offset = 1
    _r_offset = 0
    _t_offset = 0


class BuildingRotational(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 1, 2, 3, 2, 3, 0, 1)

    _m_offset = 1
    _r_offset = 2
    _t_offset = 2


class BuildingDiagonal(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 0, 1, 2, 2, 1, 3, 3)

    _m_offset = 0
    _r_offset = 1
    _t_offset = 2


class BuildingDiamond(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 0, 1, 1, 1, 1, 0, 0)

    _m_offset = 0
    _r_offset = 1
    _t_offset = 1


class BuildingCylindrical(BuildingSymmetryMixin):
    def __init__(self, obj):
        super().__init__(obj)

    _symmetry_descriptor = (0, 0, 0, 0, 0, 0, 0, 0)

    _m_offset = 0
    _r_offset = 0
    _t_offset = 0


BuildingSymmetryMixin._type_pool[(0, 1, 2, 3, 4, 5, 6, 7)] = BuildingFull
BuildingSymmetryMixin._type_pool[(0, 1, 0, 1, 2, 3, 2, 3)] = BuildingSymmetricalX
BuildingSymmetryMixin._type_pool[(0, 1, 2, 3, 0, 1, 2, 3)] = BuildingSymmetricalY
BuildingSymmetryMixin._type_pool[(0, 1, 0, 1, 0, 1, 0, 1)] = BuildingSymmetrical
BuildingSymmetryMixin._type_pool[(0, 0, 1, 2, 2, 1, 3, 3)] = BuildingDiagonal
BuildingSymmetryMixin._type_pool[(0, 1, 2, 3, 2, 3, 0, 1)] = BuildingRotational
BuildingSymmetryMixin._type_pool[(0, 0, 0, 0, 0, 0, 0, 0)] = BuildingCylindrical
