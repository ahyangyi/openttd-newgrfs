import grf
from road_vehicle.lib.standards.wheel import RadialTire, StandardProfileRadialTire, BiasPlyTire
from .balance.hog import HogCostMixin


supported_techclasses = [
    "bus",
    "2decker",
    "articulated_bus",
    "coach",
    "l_truck",
    "m_truck",
    "h_truck",
    "monorail",
    "trolleybus",
    "unknown",
]
supported_tags = ["sanctioned", "air conditioner"]


class ARoadVehicle(grf.RoadVehicle, HogCostMixin):
    def __init__(
        self,
        *,
        id,
        weight=0,
        capacity_in_tons=0,
        real_dimensions=None,
        voxel_dimensions=None,
        real_x_dimensions=None,
        axle_track=None,
        tire=None,
        tags=set(),
        techclass="unknown",
        graphics_helper=None,
        callbacks={},
        misc_flags=0,
        translation_name=None,
        **kwargs,
    ):
        self.weight_empty = weight
        self.capacity_in_tons = capacity_in_tons
        self.real_dimensions = real_dimensions
        self.real_x_dimensions = real_x_dimensions
        self.voxel_dimensions = voxel_dimensions
        self.axle_track = axle_track
        self.tire = tire
        assert all(tag in supported_tags for tag in tags)
        self.tags = tags.copy()
        assert techclass in supported_techclasses
        self.techclass = techclass
        self.graphics_helper = graphics_helper
        self.translation_name = translation_name
        if graphics_helper is not None:
            # FIXME: merge cb
            callbacks = graphics_helper.callbacks(
                my_id=id, cargo_capacity=kwargs.get("cargo_capacity", 0), feature=grf.RV
            )
        super().__init__(
            id=id,
            name=translation_name,
            liveries={},
            **{
                "weight": weight,
                "climates_available": grf.ALL_CLIMATES,
                "misc_flags": misc_flags | grf.RVFlags.USE_2CC | grf.RVFlags.AUTOREFIT | grf.RVFlags.USE_SPRITE_STACK,
                "callbacks": callbacks,
                **kwargs,
            },
        )

    def get_sprites(self, g):
        if self.translation_name is not None:
            self.name = g.strings[f"STR_VEHICLE_{self.translation_name}_NAME"]
            self.additional_text = g.strings[f"STR_VEHICLE_{self.translation_name}_DESC"]
        return super().get_sprites(g)

    @staticmethod
    def hp(x):
        return max(int(x / 10 + 0.5), 1)

    @staticmethod
    def kW(x):
        return ARoadVehicle.hp(x * 1.341022)

    @staticmethod
    def ton(x):
        return int(x * 4 + 0.5)

    @staticmethod
    def kmh(x):
        return grf.RoadVehicle.Speed(int(x * 2.01168 + 0.5))

    @staticmethod
    def kmh_from_speed(speed):
        return speed.precise_value / 2.01168

    @staticmethod
    def ton_from_weight(weight):
        return weight / 4

    def real_speed(self):
        # FIXME
        return int(ARoadVehicle.kmh_from_speed(self.max_speed) + 0.5)

    def tractive_effort(self):
        return self.ton_from_weight(self.weight_empty) * 9800 * self._props.get("tractive_effort_coefficient", 76) / 256

    def power_in_hp(self):
        return self._props["power"] * 10

    def speed_in_mph(self):
        return self.max_speed.precise_value / 0.8

    def first_gear_speed(self):
        return self.power_in_hp() * 2685.6 / self.tractive_effort()

    def equibrium_speed(self):
        axle_friction = total_weight * 10
        rolling_friction = floor((current_speed + 512) * 15 / 512) * total_weight
        air_drag_coefficient = 14 * floor(air_drag_value * (1 + number_of_parts * 3 / 20)) / 1000
        air_drag = floor(air_drag_coefficient * current_speed ^ 2)
        acceleration = (force - (slope_force + axle_friction + rolling_friction + air_drag)) / (total_weight * 4)

        p = (axle_friction + rolling_friction) / air_drag_coefficient
        q = (-power * 746 * 18 / 5) / air_drag_coefficient
        C = (27 / 2 * q + ((27 / 2 * q) ^ 2 + 27 * p ^ 3) ^ (1 / 2)) ^ (1 / 3)

        equilibrium = min(p / C - C / 3, max(0, self.tractive_effort * 1000 / air_drag_coefficient - p) ^ (1 / 2))
        return equilibrium


class ABus(ARoadVehicle):
    def __init__(self, *, id, cargo_capacity, weight=None, full_weight=None, **kwargs):
        if weight is None:
            weight = full_weight - 0.0625 * cargo_capacity
        super().__init__(
            id=id,
            capacity_in_tons=cargo_capacity / 16,
            **{"weight": ARoadVehicle.ton(weight), "cargo_capacity": cargo_capacity, **kwargs},
        )
        super().assign_hog_costs()


class ALorry(ARoadVehicle):
    def __init__(self, *, id, cargo_capacity, weight, misc_flags=0, **kwargs):
        super().__init__(
            id=id,
            capacity_in_tons=cargo_capacity,
            **{
                "weight": ARoadVehicle.ton(weight),
                "cargo_capacity": cargo_capacity,
                "misc_flags": misc_flags | grf.RVFlags.USE_CARGO_MULT,
                **kwargs,
            },
        )
        super().assign_hog_costs()


class AMonorail(ARoadVehicle):
    def __init__(self, *, id, cargo_capacity, weight=None, misc_flags=0, **kwargs):
        super().__init__(
            id=id,
            capacity_in_tons=cargo_capacity / 16,
            **{
                "weight": ARoadVehicle.ton(weight),
                "cargo_capacity": cargo_capacity,
                "misc_flags": misc_flags | grf.RVFlags.TRAM,
                **kwargs,
            },
        )
        super().assign_hog_costs()
