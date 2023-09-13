import grf


class ATrain(grf.Train):
    def __init__(
        self,
        *,
        id,
        name,
        weight=0,
        additional_text="",
        techclass="unknown",
        graphics_helper=None,
        callbacks=None,
        translation_name=None,
        **kwargs,
    ):
        self.graphics_helper = graphics_helper
        self.techclass = techclass
        self.translation_name = translation_name
        if graphics_helper is not None:
            # FIXME: merge cb
            callbacks = graphics_helper.callbacks(
                my_id=id, cargo_capacity=kwargs.get("cargo_capacity", 0), feature=grf.TRAIN
            )
        super().__init__(
            id=id,
            name=name,
            liveries={},
            **{
                "weight": weight,
                "climates_available": grf.ALL_CLIMATES,
                "misc_flags": grf.RVFlags.USE_2CC,
                "additional_text": "{SILVER}" + additional_text,
                "callbacks": callbacks,
                **kwargs,
            },
        )

    def get_sprites(self, g):
        if self.graphics_helper is not None:
            self.graphics_helper.generate_graphics()
        if self.translation_name is not None:
            self.name = g.strings[f"STR_TRAIN_{self.translation_name}_NAME"]
            self.additional_text = g.strings[f"STR_TRAIN_{self.translation_name}_DESC"]
        return super().get_sprites(g)

    def real_speed(self):
        # FIXME
        return self.max_speed
