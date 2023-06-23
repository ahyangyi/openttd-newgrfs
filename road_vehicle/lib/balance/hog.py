class HogCostMixin:
    @property
    def hog_power_points(self):
        return self.power_in_hp() / 100

    @property
    def hog_speed_points(self):
        return self.speed_in_mph() / 3

    @property
    def hog_date_points(self):
        return (self._props["introduction_date"].year - 1870) / 8

    @property
    def hog_capacity_points(self):
        return self.capacity_in_tons / 8

    @property
    def hog_points(self):
        return self.hog_power_points + self.hog_speed_points + self.hog_date_points + self.hog_capacity_points

    def assign_hog_costs(self):
        self._props["cost_factor"] = round(self.hog_points)
        self._props["running_cost_factor"] = round(self.hog_points)
