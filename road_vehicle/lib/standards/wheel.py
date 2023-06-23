class RadialTire:
    def __init__(self, width, aspect_ratio, rim_in_inches):
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.rim_in_inches = rim_in_inches

    def __str__(self):
        return f"{self.width}/{self.aspect_ratio}R{self.rim_in_inches}"

    @property
    def diameter(self):
        return self.rim_in_inches * 25.4 + self.width * 2 * self.aspect_ratio / 100


class StandardProfileRadialTire:
    def __init__(self, width_in_inches, rim_in_inches):
        self.width_in_inches = width_in_inches
        self.rim_in_inches = rim_in_inches

    def __str__(self):
        return f"{self.width_in_inches}R{self.rim_in_inches}"

    lut = {
        (11, 20): (293, 1085),
        (11, 22.5): (279, 1054),
    }

    @property
    def equivalent_width_in_inches(self):
        if self.width_in_inches <= 10:
            return self.width_in_inches + 1
        return self.width_in_inches + 0.5

    def guess_5d(self):
        return (
            self.equivalent_width_in_inches * 25.4,
            self.rim_in_inches * 25.4 + self.equivalent_width_in_inches * 25.4 * 1.97,
        )

    def guess_15d(self):
        return (self.width_in_inches * 25.4, self.rim_in_inches * 25.4 + self.width_in_inches * 25.4 * 2 * 0.88)

    def guess(self):
        if self.rim_in_inches == int(self.rim_in_inches):
            return self.guess_5d()
        return self.guess_15d()

    def look_up(self):
        return self.lut.get(
            (self.width_in_inches, self.rim_in_inches),
            self.guess(),
        )

    @property
    def diameter(self):
        return self.look_up()[1]

    @property
    def width(self):
        return self.look_up()[0]


class BiasPlyTire:
    def __init__(self, width_in_inches, rim_in_inches):
        self.width_in_inches = width_in_inches
        self.rim_in_inches = rim_in_inches

    def __str__(self):
        return f"{self.width_in_inches:.2f}-{self.rim_in_inches}"

    lut = {
        (9, 20): (259, 1018),
    }

    def look_up(self):
        return self.lut.get(
            (self.width_in_inches, self.rim_in_inches),
            self.guess(),
        )

    @property
    def equivalent_width_in_inches(self):
        if self.width_in_inches <= 10:
            return self.width_in_inches + 1
        return self.width_in_inches + 0.5

    def guess(self):
        return (
            self.equivalent_width_in_inches * 25.4,
            self.rim_in_inches * 25.4 + self.equivalent_width_in_inches * 25.4 * 1.97,
        )

    @property
    def diameter(self):
        return self.look_up()[1]

    @property
    def width(self):
        return self.look_up()[0]


if __name__ == "__main__":
    big_tire = RadialTire(275, 70, 22.5)
    print(big_tire, big_tire.diameter, big_tire.width)

    old_tire = StandardProfileRadialTire(11, 22.5)
    print(old_tire, old_tire.diameter, old_tire.width, old_tire.guess())

    old_tire = StandardProfileRadialTire(11, 20)
    print(old_tire, old_tire.diameter, old_tire.width, old_tire.guess())

    really_old_tire = BiasPlyTire(9, 20)
    print(really_old_tire, really_old_tire.diameter, really_old_tire.width, really_old_tire.guess())
