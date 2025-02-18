def make_tuple(x):
    if isinstance(x, tuple):
        return x
    return (x,)


def optional_to_tuple(x):
    if x is None:
        return ()
    return (x,)


class Industry:
    @property
    def translated_accepts(self):
        return bytes(cargo.translated_id for cargo in self.accepts)

    @property
    def translated_produces(self):
        return bytes(cargo.translated_id for cargo in self.produces)


class PrimaryIndustry(Industry):
    def __init__(self, produces=(), extra_accepts=(), boosters=()):
        self.produces = make_tuple(produces)
        self.extra_accepts = make_tuple(extra_accepts)
        self._boosters = make_tuple(boosters)

    def copy(self):
        return PrimaryIndustry(self.produces, self.extra_accepts, self.boosters)

    @property
    def accepts(self):
        return self.extra_accepts + self.boosters

    @property
    def consumes(self):
        return ()

    @property
    def boosters(self):
        return self._boosters

    @boosters.setter
    def boosters(self, new_boosters):
        self._boosters = make_tuple(new_boosters)

    def to_secondary(self, consumes):
        return FakePrimaryIndustry(consumes, self.produces, self.extra_accepts, self.boosters)


class WorkerYard(PrimaryIndustry):
    def __init__(self, produces=(), extra_accepts=(), boosters=()):
        super().__init__(produces, extra_accepts, boosters)


class FreePort(PrimaryIndustry):
    def __init__(self, boosters=(), produces=(), extra_accepts=()):
        super().__init__(produces, extra_accepts, boosters)


class SecondaryIndustry(Industry):
    def __init__(self, consumes=(), produces=(), extra_accepts=(), boosters=()):
        self.consumes = make_tuple(consumes)
        self.produces = make_tuple(produces)
        self.extra_accepts = make_tuple(extra_accepts)
        self._boosters = make_tuple(boosters)

    def copy(self):
        return SecondaryIndustry(self.consumes, self.produces, self.extra_accepts, self.boosters)

    @property
    def boosters(self):
        return self._boosters

    @boosters.setter
    def boosters(self, new_boosters):
        self._boosters = make_tuple(new_boosters)

    @property
    def accepts(self):
        return self.consumes + self.extra_accepts + self.boosters


class FakePrimaryIndustry(SecondaryIndustry):
    def __init__(self, consumes=(), produces=(), extra_accepts=(), boosters=()):
        super().__init__(consumes, produces, extra_accepts, boosters)


class TertiaryIndustry(Industry):
    def __init__(self, consumes=()):
        self.consumes = make_tuple(consumes)

    def copy(self):
        return TertiaryIndustry(self.consumes)

    @property
    def accepts(self):
        return self.consumes

    @property
    def produces(self):
        return ()


class Town(Industry):
    def __init__(self, passengers, mail, food, goods):
        self.passengers = passengers
        self.mail = mail
        self.food = food
        self.goods = goods

    def copy(self):
        return Town(self.passengers, self.mail, self.food, self.goods)

    @property
    def accepts(self):
        return tuple(y for x in (self.passengers, self.mail, self.food, self.goods) for y in optional_to_tuple(x))

    @property
    def consumes(self):
        return ()

    @property
    def produces(self):
        return tuple(y for x in (self.passengers, self.mail) for y in optional_to_tuple(x))
